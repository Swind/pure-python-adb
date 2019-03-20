import time
from adb.plugins.device.utils import Activity


def open_chrome(device):
    activity = "com.android.chrome/com.google.android.apps.chrome.Main"
    cmd = 'am start -a android.intent.action.VIEW -n {activity} -d {url}'.format(
        activity=activity,
        url="https://www.google.com"
    )
    device.shell(cmd)


def test_get_traffic(device):
    open_chrome(device)
    time.sleep(5)
    # Get chrome traffic state
    states = device.get_traffic("com.android.chrome")

    assert states is not None
    assert len(states) != 0


def test_get_traffic_of_not_existing_package(device):
    states = device.get_traffic("com.not.existing.package")

    assert states is None


def test_get_cpu_stat(device):
    open_chrome(device)

    pid = device.get_pid("com.android.chrome")
    assert pid is not None

    total_cpu_stat = device.get_total_cpu()
    process_cpu_stat = device.get_pid_cpu(pid)

    print("CPU Total: {}\n".format(total_cpu_stat))
    print("CPU Process: {}\n".format(process_cpu_stat))

    assert total_cpu_stat is not None
    assert process_cpu_stat is not None


def test_get_top_activities(device):
    result = device.get_top_activities()
    assert result
    assert isinstance(result, list)
    for i in result:
        assert isinstance(i, Activity)
        assert hasattr(i, 'package')
        assert isinstance(i.package, str)
        assert hasattr(i, 'activity')
        assert isinstance(i.activity, str)
        assert hasattr(i, 'pid')
        assert isinstance(i.pid, str)


def test_get_top_activity(device):
    result = device.get_top_activity()
    assert isinstance(result, Activity)
