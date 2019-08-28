def test_get_cpu_times(device):
    result = device.cpu_times()
    assert result is not None

def test_get_cpu_percent(device):
    percent = device.cpu_percent(interval=1)
    assert percent is not None
    assert percent != 0

def test_get_cpu_count(device):
    assert device.cpu_count() == 2
