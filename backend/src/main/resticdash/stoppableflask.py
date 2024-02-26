from threading import Thread, Event
from typing import List

from flask import Flask, Blueprint
from flask_cors import CORS
from waitress import serve


class StoppableFlask(Thread):
    """
    A thread to run Flask allowing it to be stopped as the original shutdown functionality of the
    Flask server isn't really accessible.
    """

    def __init__(self, name: str, port: int = 8080, timeout=0.5, origins: List[str] = []):
        self._flask = Flask(name)
        if len(origins) > 0:
            CORS(self._flask, resources={r"/*": {"origins": origins}})
        super().__init__(target=self._target)
        self._stopped = Event()
        self._timeout = timeout
        self._port = port

    def _target(self):
        serve(self._flask, host='0.0.0.0', port=self._port, threads=20)

    def register_blueprint(self, blueprint: Blueprint, prefix: str):
        self._flask.register_blueprint(blueprint, url_prefix=prefix)

    def stop(self):
        self._stopped.set()

    def execute(self):
        self._stopped.clear()
        self.start()
        while not self._stopped.is_set():
            try:
                super().join(self._timeout)
            except KeyboardInterrupt:
                self._stopped.set()
