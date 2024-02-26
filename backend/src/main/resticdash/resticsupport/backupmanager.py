import logging
import os

from threading import Event, Thread

from watchdog.events import FileSystemEventHandler, EVENT_TYPE_DELETED
from watchdog.observers import Observer
from typing import List, Optional

from resticdash.config import CfgResticDash
from resticdash.resticsupport.backupdata import BackupData
from resticdash.resticsupport.responses import BackupInfos
from resticdash.utils.dirtymap import DirtyMap

logger = logging.getLogger(__name__)


class LockFileDeletedCallback(FileSystemEventHandler):
    """
    Invokes a function if a deletion event occurred on a file.
    """

    def __init__(self, function):
        self.function = function

    def on_any_event(self, event):
        if event.is_directory or event.is_synthetic or event.event_type != EVENT_TYPE_DELETED:
            # not of interest
            return
        self.function()


class BackupManager(Thread):
    """
    This helper is responsible to watch over all repositories and load their backup status.
    """

    stop_event: Event
    dirty_map: DirtyMap

    def __init__(self, cfg: CfgResticDash):
        super().__init__(target = self.watch)
        self.cfg = cfg
        self.stop_event = Event()
        self.backup_data = BackupData(cfg.backups)
        self.dirty_map = DirtyMap()

    def _start_observer(self) -> Observer:
        logger.info("Starting to watch repositories ...")
        result = Observer()
        logger.info(f"Got {len(self.cfg.backups)} backup records !")
        for name, cfg_backup in self.cfg.backups.items():
            locks_dir = os.path.join(cfg_backup.repository, 'locks')
            logger.debug(f"Observing directory '{locks_dir}'")
            result.schedule(LockFileDeletedCallback(lambda n=name: self.dirty_map.dirty(n)), locks_dir)
        result.start()
        return result

    def _stop_observer(self, observer: Observer):
        logger.info("Stopping to watch repositories ...")
        try:
            observer.stop()
        except Exception as ex:
            logger.error("Failed to stop observer", exc_info=ex)

    def watch(self):

        self.stop_event.clear()
        observer = self._start_observer()

        while not self.stop_event.is_set():
            interrupted = self.stop_event.wait(60)
            if not interrupted:
                # the timer ran out, so we're continuing normally
                outdated = self.dirty_map.get_outdated(self.cfg.settings.delay)
                for name in outdated:
                    self.dirty_map.clear(name)
                    self.backup_data.update(name)

        self._stop_observer(observer)

    def stop(self):
        self.stop_event.set()

    def get_backup_infos(self, name: str) -> Optional[BackupInfos]:
        return self.backup_data.get_backup_infos(name)

    def get_all_backup_infos(self) -> List[BackupInfos]:
        return self.backup_data.get_all_backup_infos()
