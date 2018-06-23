This is pure-python implementation of the ADB client.

You can use it to communicate with adb server (not the adb daemon on the device/emulator).

Installation
============

.. code-block:: console

    $pip install -U pure-python-adb

Examples
========

Connect to adb server and get the version
-----------------------------------------

.. code-block:: python

    from adb.client import Client as AdbClient
    # Default is "127.0.0.1" and 5037
    client = AdbClient(host="127.0.0.1", port=5037)
    print(client.version())

    >>> 39

Connect to a device
-------------------

.. code-block:: python

    from adb.client import Client as AdbClient
    # Default is "127.0.0.1" and 5037
    client = AdbClient(host="127.0.0.1", port=5037)
    device = client.device("emulator-5554")


List all devices ( adb devices ) and install/uninstall an APK on all devices
----------------------------------------------------------------------------

.. code-block:: python

    from adb.client import Client as AdbClient

    apk_path = "example.apk"

    # Default is "127.0.0.1" and 5037
    client = AdbClient(host="127.0.0.1", port=5037)
    devices = client.devices()

    for device in devices:
        device.install(apk_path)

    # Check apk is installed
    for device in devices:
        print(device.is_installed("example.package"))

    # Uninstall
    for device in devices:
        device.uninstall("example.package)

adb shell
---------

.. code-block:: python

    from adb.client import Client as AdbClient
    # Default is "127.0.0.1" and 5037
    client = AdbClient(host="127.0.0.1", port=5037)
    device = client.device("emulator-5554")
    device.shell("echo hello world !")

.. code-block:: python

    def dump_logcat(connection):
        while True:
            data = connection.read(1024)
            if not data:
                break
            print(data.decode('utf-8')))

        connection.close()

    from adb.client import Client as AdbClient
    # Default is "127.0.0.1" and 5037
    client = AdbClient(host="127.0.0.1", port=5037)
    device = client.device("emulator-5554")
    device.shell("logcat", handler=dump_logcat)


Screenshot
----------

.. code-block:: python

    from adb.client import Client as AdbClient
    client = AdbClient(host="127.0.0.1", port=5037)
    device = client.device("emulator-5554")
    result = device.screencap()
    with open("screen.png", "wb") as fp:
        fp.write(result)

Push
----

.. code-block:: python

    from adb.client import Client as AdbClient
    client = AdbClient(host="127.0.0.1", port=5037)
    device = client.device("emulator-5554")

    device.push("example.apk", "/sdcard/example.apk")

Pull
----

.. code-block:: python

    from adb.client import Client as AdbClient
    client = AdbClient(host="127.0.0.1", port=5037)
    device = client.device("emulator-5554")

    device.shell("screencap -p /sdcard/screen.png")
    device.pull("/sdcard/screen.png", "screen.png")
