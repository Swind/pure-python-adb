from adb.device import Device


class Application:
    def __init__(self, device: Device, package: str):
        self._device = device
        self._package = package

    def pid(self):
        pass

    def uid(self):
        pass

    @property
    def tcp_recv(self) -> int:
        return 0

    @property
    def tcp_send(self) -> int:
        return 0
