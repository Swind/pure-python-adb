try:
    from asyncio import get_running_loop
except ImportError:  # pragma: no cover
    from asyncio import get_event_loop as get_running_loop  # Python 3.6 compatibility

import re
import os

from ppadb import InstallError
from ppadb.command.transport_async import TransportAsync
from ppadb.sync_async import SyncAsync

from ppadb.utils.logger import AdbLogging

try:
    from shlex import quote as cmd_quote
except ImportError:
    from pipes import quote as cmd_quote


logger = AdbLogging.get_logger(__name__)


def _get_src_info(src):
    exists = os.path.exists(src)
    isfile = os.path.isfile(src)
    isdir = os.path.isdir(src)
    basename = os.path.basename(src)
    walk = None if not isdir else list(os.walk(src))

    return exists, isfile, isdir, basename, walk


class DeviceAsync(TransportAsync):
    INSTALL_RESULT_PATTERN = "(Success|Failure|Error)\s?(.*)"
    UNINSTALL_RESULT_PATTERN = "(Success|Failure.*|.*Unknown package:.*)"

    def __init__(self, client, serial):
        self.client = client
        self.serial = serial

    async def create_connection(self, set_transport=True, timeout=None):
        conn = await self.client.create_connection(timeout=timeout)

        if set_transport:
            await self.transport(conn)

        return conn

    async def _push(self, src, dest, mode, progress):
        # Create a new connection for file transfer
        sync_conn = await self.sync()
        sync = SyncAsync(sync_conn)

        async with sync_conn:
            await sync.push(src, dest, mode, progress)

    
    async def install(self, path,
                forward_lock=False,  # -l
                reinstall=False,  # -r
                test=True,  # -t
                installer_package_name="",  # -i {installer_package_name}
                shared_mass_storage=False,  # -s
                internal_system_memory=False,  # -f
                downgrade=False,  # -d
                grand_all_permissions=True  # -g
                ):
        dest = SyncAsync.temp(path)

        parameters = []
        if forward_lock: parameters.append("-l")
        if reinstall: parameters.append("-r")
        if test: parameters.append("-t")
        if len(installer_package_name) > 0: parameters.append("-i {}".format(installer_package_name))
        if shared_mass_storage: parameters.append("-s")
        if internal_system_memory: parameters.append("-f")
        if downgrade: parameters.append("-d")
        if grand_all_permissions: parameters.append("-g")

        try:
            result = await self.shell(
                "pm install {} {}".format(" ".join(parameters), cmd_quote(dest))
            )
            match = re.search(self.INSTALL_RESULT_PATTERN, result)

            if match and match.group(1) == "Success":
                return True
            elif match:
                groups = match.groups()
                raise InstallError(dest, groups[1])
            else:
                raise InstallError(dest, result)
        finally:
            await self.shell("rm -f {}".format(dest))

    async def uninstall(self, package="com.github.uiautomator2"):
        result = await self.shell("pm uninstall {}".format(package))

        m = re.search(self.UNINSTALL_RESULT_PATTERN, result)

        if m and m.group(1) == "Success":
            return True
        elif m:
            logger.error(m.group(1))
            return False
        else:
            logger.error("There is no message after uninstalling")
            return False

    async def push(self, src, dest, mode=0o644, progress=None):
        exists, isfile, isdir, basename, walk = await get_running_loop().run_in_executor(None, _get_src_info, src)
        if not exists:
            raise FileNotFoundError("Cannot find {}".format(src))

        if isfile:
            await self._push(src, dest, mode, progress)

        elif isdir:
            for root, dirs, files in walk:
                root_dir_path = os.path.join(basename, root.replace(src, ""))

                await self.shell("mkdir -p {}/{}".format(dest, root_dir_path))

                for item in files:
                    await self._push(os.path.join(root, item), os.path.join(dest, root_dir_path, item), mode, progress)

    async def pull(self, src, dest):
        sync_conn = await self.sync()
        sync = SyncAsync(sync_conn)

        async with sync_conn:
            return await sync.pull(src, dest)