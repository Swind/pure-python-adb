def test_list_devices(client):
    devices = client.devices()

    assert len(devices) > 0
    assert any(map(lambda device: device.serial == "emulator-5554", devices))


def test_version(client):
    version = client.version()

    assert type(version) == int
    assert version != 0

def test_list_forward(client, device):
    client.killforward_all()
    result = client.list_forward()
    assert not result

    device.forward("tcp:6000", "tcp:6000")
    result = client.list_forward()
    assert result["emulator-5554"]["tcp:6000"] == "tcp:6000"

    client.killforward_all()
    result = client.list_forward()
    assert not result


def test_features(client):
    assert client.features()
