import threading


def test_shell_sync(device):
    result = device.shell("dumpsys")
    assert "dumpsys window sessions" in result


def test_shell_async(device):
    result = b''

    def callback(conn):
        nonlocal result
        while True:
            data = conn.read(1024)
            if not data:
                break
            result += data

    thread = threading.Thread(target=device.shell, args=("dumpsys", callback))
    thread.start()
    thread.join()

    assert "dumpsys window sessions" in result.decode('utf-8')


def test_get_device_path(device):
    result = device.get_device_path()
    assert result == 'unknown'


def test_get_serial_no(device):
    result = device.get_serial_no()
    assert result == 'emulator-5554'


def test_get_state(device):
    result = device.get_state()
    assert result == 'device'
