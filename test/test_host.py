import time

def test_list_devices(client, serial):
    devices = client.devices()
    assert len(devices) > 0
    assert any(map(lambda device: device.serial == serial, devices))

def test_list_devices_by_state(client):
    devices = client.devices(client.BOOTLOADER)
    assert len(devices) == 0

    devices = client.devices(client.OFFLINE)
    assert len(devices) == 0

    devices = client.devices(client.DEVICE)
    assert len(devices) == 1

def test_version(client):
    version = client.version()

    assert type(version) == int
    assert version != 0

def test_list_forward(client, device, serial):
    client.killforward_all()
    result = client.list_forward()
    assert not result

    device.forward("tcp:6000", "tcp:6000")
    result = client.list_forward()
    assert result[serial]["tcp:6000"] == "tcp:6000"

    client.killforward_all()
    result = client.list_forward()
    assert not result


def test_features(client):
    assert client.features()


def test_remote_connect_disconnect(client):
    host = client.host
    client.remote_connect(host, 5555)
    device = client.device("{}:5555".format(host))
    assert device is not None

    # Disconnect by ip
    client.remote_disconnect(host)
    device = client.device("{}:5555".format(host))
    assert device is None

    # Disconnect by ip and port
    client.remote_connect(host, 5555)
    device = client.device("{}:5555".format(host))
    assert device is not None

    # Disconnect all
    client.remote_disconnect()
    device = client.device("{}:5555".format(host))
    assert device is None

    for index in range(0, 10):
        device = client.device("emulator-5554")
        if device is not None:
            break
        else:
            time.sleep(1)

    assert device is not None
