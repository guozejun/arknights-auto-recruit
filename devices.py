import subprocess
import time

def get_devices_no() -> str:
    output = subprocess.check_output("adb devices", stderr=subprocess.STDOUT, shell=True)
    devices_no = output.splitlines()[1].split(b'\t')[0].decode('utf-8')
    return devices_no

class devices:
    def __init__(self, devices_no):
        self.__devices_no = devices_no

    def __get_time_stamp(self) -> str:
        return time.ctime().replace(' ', '-').lower()

    def get_screenshot(self) -> str:
        devices_no = self.__devices_no
        stamp = self.__get_time_stamp()
        result = subprocess.run('adb -s {} exec-out screencap -p > ./img/{}.png'.format(devices_no, stamp), shell=True, check=True)
        if result.returncode == 0:
            return stamp
        else:
            return None