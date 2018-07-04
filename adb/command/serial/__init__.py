from adb.command import Command


class Serial(Command):
    def _execute_cmd(self, cmd, set_transport):
        conn = self.create_connection(set_transport=set_transport)

        with conn:
            conn.send(cmd)
            result = conn.receive()
            return result

    def forward(self, local, remote):
        cmd = "host-serial:{serial}:forward:{local};{remote}".format(
            serial=self.serial,
            local=local,
            remote=remote)
        self._execute_cmd(cmd, set_transport=False)

    def list_forward(self):
        cmd = "host-serial:{serial}:list-forward".format(serial=self.serial)
        result = self._execute_cmd(cmd, set_transport=False)

        forward_map = {}

        for line in result.split('\n'):
            if line:
                _, local, remote = line.split()
                forward_map[local] = remote

        return forward_map

    def get_device_path(self):
        cmd = "host-serial:{serial}:get-devpath".format(serial=self.serial)
        return self._execute_cmd(cmd, set_transport=False)

    def get_serial_no(self):
        cmd = "host-serial:{serial}:get-serialno".format(serial=self.serial)
        return self._execute_cmd(cmd, set_transport=False)

    def get_state(self):
        cmd = "host-serial:{serial}:get-state".format(serial=self.serial)
        return self._execute_cmd(cmd, set_transport=False)
