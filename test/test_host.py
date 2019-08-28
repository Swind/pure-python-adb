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
