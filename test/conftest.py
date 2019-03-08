import time
import telnetlib
import logging

import pytest

from adb.client import Client as AdbClient
from adb.device import Device as AdbDevice

logger = logging.getLogger(__name__)

adb_host = "emulator"
# adb_host = "172.19.0.2"
# adb_host = "127.0.0.1"
adb_port = 5037
emulator_port = 5554


class EmulatorConsole:
    def __init__(self, host, port):
        self._port = port
        self._telnet = telnetlib.Telnet(host=host, port=port)
        print(self._telnet.read_until(b"OK", timeout=5))

    def send(self, data):
        self._telnet.write(data.encode('utf-8') + b'\n')
        return self._telnet.read_until(b"OK", timeout=5).decode('utf-8').strip()

    def is_live(self):
        result = self.send("ping")
        if "I am alive!" in result:
            return True
        else:
            return False

    def kill(self):
        self.send("kill")
        return True


def wait_until_true(check_fn, timeout=10, description=None, interval=1):
    start_time = time.time()
    duration = 0
    while True:
        elapsed_seconds = time.time() - start_time
        if elapsed_seconds >= timeout:
            return False

        if check_fn():
            return True
        else:
            if description:
                msg = description
            else:
                msg = "Wait until {} return True...".format(check_fn.__name__ + "()")

            elapsed_seconds = int(elapsed_seconds)
            if duration != elapsed_seconds:
                duration = elapsed_seconds
                logger.info("{}... {}s (timeout:{})".format(msg, elapsed_seconds, timeout))

            time.sleep(interval)


@pytest.fixture(scope="session")
def client(request):
    logger.info("Connecting to adb server {}:{}...".format(adb_host, adb_port))
    client = AdbClient(host=adb_host, port=adb_port)

    def try_to_connect_to_adb_server():
        try:
            client.version()
            return True
        except Exception:
            return False

    wait_until_true(try_to_connect_to_adb_server,
                    timeout=60,
                    description="Try to connect to adb server {}:{}".format(adb_host, adb_port))

    logger.info("Adb server version: {}".format(client.version()))

    return client


@pytest.fixture(scope="session")
def device(request, client):
    def emulator_console_is_connectable():
        try:
            console = EmulatorConsole(host=adb_host, port=emulator_port)
            return console
        except Exception as e:
            return None

    def is_boot_completed():
        try:
            adb_device = client.device("emulator-5554")
            result = adb_device.shell("getprop sys.boot_completed")
            if not result:
                return False

            result = int(result.strip())

            if result == 1:
                return True
            else:
                return False
        except ValueError as e:
            logger.warning(e)
            return False
        except Exception as e:
            logger.error(e)
            return False

    result = wait_until_true(emulator_console_is_connectable, timeout=60)
    assert result, "Can't connect to the emulator console"

    result = wait_until_true(is_boot_completed, timeout=60)
    assert result, "The emulator doesn't boot"

    return AdbDevice(client, "emulator-5554")
