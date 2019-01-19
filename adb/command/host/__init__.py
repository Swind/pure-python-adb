from adb.device import Device
from adb.command import Command


class Host(Command):
    CONNECT_RESULT_PATTERN = "(connected to|already connected)"

    def _execute_cmd(self, cmd, with_response=True):
        with self.create_connection() as conn:
            conn.send(cmd)
            if with_response:
                result = conn.receive()
                return result
            else:
                conn.check_status()

    def devices(self):
        cmd = "host:devices"
        result = self._execute_cmd(cmd)

        devices = []

        for line in result.split('\n'):
            if not line:
                break

            tokens = line.split()
            devices.append(Device(self, tokens[0]))

        return devices

    def version(self):
        with self.create_connection() as conn:
            conn.send("host:version")
            version = conn.receive()
            return int(version, 16)

    def kill(self):
        """
            Ask the ADB server to quit immediately. This is used when the
            ADB client detects that an obsolete server is running after an
            upgrade.
        """
        with self.create_connection() as conn:
            conn.send("host:kill")

        return True

    def killforward_all(self):
        cmd = "host:killforward-all"
        self._execute_cmd(cmd, with_response=False)

    def list_forward(self):
        cmd = "host:list-forward"
        result = self._execute_cmd(cmd)

        device_forward_map = {}
        for line in result.split('\n'):
            if line:
                serial, local, remote = line.split()
                if serial not in device_forward_map:
                    device_forward_map[serial] = {}

                device_forward_map[serial][local] = remote

        return device_forward_map
