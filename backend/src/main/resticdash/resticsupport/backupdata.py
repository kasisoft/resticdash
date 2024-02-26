import logging
import restic

from datetime import datetime, timedelta, timezone
from threading import Lock
from typing import Dict, List, Optional

from resticdash.config import CfgResticDash, CfgBackup
from resticdash.resticsupport.responses import BackupInfos, SnapshotInfo

logger = logging.getLogger(__name__)


class BackupData:
    """
    Just a store for all backup configurations.
    """

    backup_infos: Dict[str, BackupInfos]

    def __init__(self, cfg: Dict[str, CfgBackup]):
        self.cfg = cfg
        self.backup_infos = {}
        self.mutex = Lock()
        for name in self.cfg.keys():
            self.update(name)

    def _create_snapshots(self, json_result: List[Dict]) -> List[SnapshotInfo]:
        result: List[SnapshotInfo] = []
        for json_record in json_result:
            try:
                result.append(SnapshotInfo.from_dict(json_record))
            except Exception as ex:
                # shouldn't happen but better be safe
                logger.error(f"Failed to deserialize snapshot info: {json_record}", exc_info=ex)
        return result

    def update(self, name: str):

        logger.info(f"Loading backup data for '{name} ...")
        with self.mutex:

            try:
                cfg_backup: CfgBackup = self.cfg[name]

                restic.repository = cfg_backup.repository
                restic.password_file = cfg_backup.password
                restic.use_cache = False

                # fetch the json result from our repository
                json_result: List[Dict] = restic.snapshots("--no-lock")
                logger.debug(f"Found {len(json_result)} snapshot records for '{name}'")

                # store the outcome
                self.backup_infos[name] = BackupInfos(
                    name,
                    cfg_backup.backup_fail_delay,
                    self._create_snapshots(json_result)
                )

            except Exception as ex:
                logger.error(f"Failed to execute restic for {name}", exc_info=ex)

        logger.info(f"Loading backup for {name} concluded")

    def get_backup_infos(self, name: str) -> Optional[BackupInfos]:
        with self.mutex:
            return self.backup_infos.get(name, None)

    def get_all_backup_infos(self) -> List[BackupInfos]:
        with self.mutex:
            return list(self.backup_infos.values())
