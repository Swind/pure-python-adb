import threading
import pytest


def test_shell_sync(device):
    result = device.shell("dumpsys")
    assert "dumpsys window sessions" in result


def test_shell_async(device):
    result = bytearray()

    def callback(conn):
        while True:
            data = conn.read(1024)
            if not data:
                break
            result.extend(bytearray(data))

    thread = threading.Thread(target=device.shell, args=("dumpsys", callback))
    thread.start()
    thread.join()

    assert "dumpsys window sessions" in result.decode('utf-8')


def test_get_device_path(device):
    result = device.get_device_path()
    assert result == 'unknown'


def test_get_serial_no(device, serial):
    result = device.get_serial_no()
    assert result == serial


def test_get_state(device):
    result = device.get_state()
    assert result == 'device'


def test_forward(device):
    device.forward("tcp:9999", "tcp:7777")
    forward_list = device.list_forward()
    assert "tcp:9999" in forward_list
    assert forward_list['tcp:9999'] == "tcp:7777"

    device.killforward("tcp:9999")
    forward_list = device.list_forward()
    assert len(forward_list) == 0


def test_forward_killforward_all(device):
    device.forward("tcp:9999", "tcp:7777")
    forward_list = device.list_forward()
    assert "tcp:9999" in forward_list
    assert forward_list['tcp:9999'] == "tcp:7777"

    device.killforward_all()
    forward_list = device.list_forward()
    assert len(forward_list) == 0


def test_forward_norebind_failed(device):
    try:
        device.forward("tcp:9999", "tcp:7777")
        forward_list = device.list_forward()
        assert "tcp:9999" in forward_list
        assert forward_list['tcp:9999'] == "tcp:7777"

        with pytest.raises(RuntimeError) as excinfo:
            device.forward("tcp:9999", "tcp:7777", norebind=True)

        assert "cannot rebind existing socket" in str(excinfo.value)
    finally:
        device.killforward_all()
        forward_list = device.list_forward()
        assert len(forward_list) == 0
