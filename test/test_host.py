def test_list_devices(client):
    devices = client.devices()

    assert len(devices) > 0
    assert any(map(lambda device: device.serial == "emulator-5554", devices))


def test_version(client):
    version = client.version()

    assert type(version) == int
    assert version != 0
