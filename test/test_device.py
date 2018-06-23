import os

import pytest
import socket

from adb import ClearError


def test_install_uninstall_success(device):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    result = device.install(os.path.join(dir_path, "resources/apk/app-x86.apk"))
    assert result is True

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

    with pytest.raises(ClearError, message="Package com.android.not.exist.package could not be cleared - [Failed]"):
        result = device.clear("com.android.not.exist.package")


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
    with pytest.raises(socket.timeout, message="cmd `sleep 60;echo passed` should be timeout"):
        device.shell("sleep 60;echo passed", timeout=10)


def test_get_top_activity(device):
    activity = device.get_top_activity()
    assert activity is not None


def test_get_top_activities(device):
    activities = device.get_top_activities()
    assert len(activities) != 0
