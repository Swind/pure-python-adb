import logging

from adb.command.host import Host
from adb.connection import Connection

logger = logging.getLogger(__name__)


class Client(Host):
    def __init__(self, host='127.0.0.1', port=5037):
        self.host = host
        self.port = port

    def create_connection(self, timeout=None):
        conn = Connection(self.host, self.port, timeout)
        conn.connect()
        return conn

    def device(self, serial: str):
        devices = self.devices()

        for device in devices:
            if device.serial == serial:
                return device

        return None
