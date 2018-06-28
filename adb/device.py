import shlex
import re
import os

from adb.command.transport import Transport
from adb.command.serial import Serial

from adb.plugins.device.input import Input
from adb.plugins.device.utils import Utils
from adb.plugins.device.wm import WM
from adb.plugins.device.traffic import Traffic
from adb.plugins.device.stat import Stat

from adb.sync import Sync

from adb.utils.logging import get_logger

from adb import InstallError

logger = get_logger(__name__)


class Device(Transport, Serial, Input, Utils, WM, Traffic, Stat):
    INSTALL_RESULT_PATTERN = "(Success|Failure|Error)\s?(.*)"
    UNINSTALL_RESULT_PATTERN = "(Success|Failure.*|.*Unknown package:.*)"

    def __init__(self, client, serial):
        self.client = client
        self.serial = serial

    def create_connection(self, set_transport=True, timeout=None):
        conn = self.client.create_connection(timeout=timeout)
        conn.connect()

        if set_transport:
            self.transport(conn)

        return conn

    def push(self, src, dest, mode=0o644):
        if not os.path.exists(src):
            raise FileNotFoundError("Cannot find {}".format(src))

        # Create a new connection for file transfer
        sync_conn = self.sync()
        sync = Sync(sync_conn)

        with sync_conn:
            sync.push(src, dest, mode)

    def pull(self, src, dest):
        sync_conn = self.sync()
        sync = Sync(sync_conn)

        with sync_conn:
            return sync.pull(src, dest)

    def install(self, path):
        dest = Sync.temp(path)
        self.push(path, dest)

        try:
            result = self.shell("pm install -r {}".format(shlex.quote(dest)))
            match = re.search(self.INSTALL_RESULT_PATTERN, result)

            if match and match.group(1) == "Success":
                return True
            elif match:
                groups = match.groups()
                raise InstallError(dest, groups[1])
            else:
                raise InstallError(dest, result)
        finally:
            self.shell("rm -f {}".format(dest))

    def is_installed(self, package):
        result = self.shell('pm path {}'.format(package))

        if "package:" in result:
            return True
        else:
            return False

    def uninstall(self, package):
        result = self.shell('pm uninstall {}'.format(package))

        m = re.search(self.UNINSTALL_RESULT_PATTERN, result)

        if m and m.group(1) == "Success":
            return True
        elif m:
            logger.error(m.group(1))
            return False
        else:
            logger.error("There is no message after uninstalling")
            return False
