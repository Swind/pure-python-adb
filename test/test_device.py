import os

import pytest
import socket

from adb import ClearError, InstallError


def test_install_uninstall_success(device):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    result = device.install(os.path.join(dir_path, "resources/apk/app-x86.apk"),
                            reinstall=True,
                            downgrade=True)
    assert result is True

    with pytest.raises(InstallError) as excinfo:
        device.install(os.path.join(dir_path, "resources/apk/app-x86.apk"))

    assert "INSTALL_FAILED_ALREADY_EXISTS" in str(excinfo.value)

    result = device.is_installed('com.cloudmosa.helloworldapk')
    assert result is True

    result = device.uninstall("com.cloudmosa.helloworldapk")
    assert result is True

    result = device.uninstall("com.cloudmosa.helloworldapk")
    assert result is False

    result = device.is_installed('com.cloudmosa.helloworldapk')
    assert result is False


def test_uninstall_not_exist_package(device):
    result = device.uninstall("com.cloudmosa.not.exist")
    assert result is False


def test_list_features(device):
    features = device.list_features()
    assert "reqGlEsVersion" in features
    assert "android.hardware.sensor.barometer" in features

    assert features["reqGlEsVersion"] == "0x20000"
    assert features["android.hardware.sensor.barometer"] is True


def test_clear(device):
    result = device.clear("com.android.chrome")
    assert result is True

    with pytest.raises(ClearError) as excinfo:
        result = device.clear("com.android.not.exist.package")

    assert "Package com.android.not.exist.package could not be cleared - [Failed]" in str(excinfo.value)


def test_list_packages(device):
    packages = device.list_packages()

    assert "com.android.chrome" in packages
    assert "com.android.shell" in packages


def test_get_properties(device):
    properties = device.get_properties()

    assert "ro.product.device" in properties
    assert "ro.product.model" in properties


def test_list_reverses(device):
    result = device.list_reverses()
    assert result is not None


def test_reboot_than_wait_boot(device):
    result = device.reboot()
    assert device.wait_boot_complete() is True


def test_get_version_name(device):
    result = device.get_package_version_name("com.android.chrome")
    assert result is not None


def test_shell_echo_sleep_long_time(device):
    result = device.shell("sleep 30;echo passed")
    assert "passed" in result


def test_shell_echo_timeout(device):
    with pytest.raises(socket.timeout) as excinfo:
        device.shell("sleep 60;echo passed", timeout=10)

    assert "timed out" in str(excinfo.value)


def test_get_top_activity(device):
    activity = device.get_top_activity()
    assert activity is not None


def test_get_top_activities(device):
    activities = device.get_top_activities()
    assert len(activities) != 0


def test_push_and_pull(device):
    import hashlib

    device.shell("screencap -p /sdcard/screen.png")
    checksum = device.shell("md5sum -b /sdcard/screen.png").strip()

    device.pull("/sdcard/screen.png", "./screen.png")
    hash_md5 = hashlib.md5()
    with open("./screen.png", "rb") as fp:
        for chunk in iter(lambda: fp.read(4096), b""):
            hash_md5.update(chunk)

    pull_checksum = hash_md5.hexdigest()

    assert checksum == pull_checksum


def test_forward(device):
    device.killforward_all()
    forward_map = device.list_forward()
    assert not forward_map

    device.forward("tcp:6000", "tcp:7000")
    forward_map = device.list_forward()
    assert forward_map['tcp:6000'] == "tcp:7000"

    device.killforward_all()
    forward_map = device.list_forward()
    assert not forward_map



