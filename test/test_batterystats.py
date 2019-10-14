import pytest

@pytest.mark.skip
def test_get_batterystats(device):
    assert device.get_batterystats() is not None

def test_get_battery_level(device):
    result = device.get_battery_level()
    assert result == 100
