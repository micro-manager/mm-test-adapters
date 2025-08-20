import os

from mm_test_adapters import device_adapter_path


def test_path():
    path = device_adapter_path()
    assert os.listdir(path) == [
        "DeviceAdapters/DemoCamera",
        "DeviceAdapters/Utilities",
        "DeviceAdapters/NotificationTester",
        "DeviceAdapters/SequenceTester",
    ]
