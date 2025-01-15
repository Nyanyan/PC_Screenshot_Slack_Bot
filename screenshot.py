
IMG_FILE = 'hoge'
CHANNEL = 'hoge'
PC_NAME = 'hoge'
CHANNEL_ID = 'hoge'
TOKEN = 'hoge'

from slack_sdk import WebClient
import pyautogui
import psutil
import datetime
import wmi

#import os
#slack_token = os.environ["SLACK_PC_SCREEN_SENDER_TOKEN"]
#client = WebClient(token=slack_token)

def get_cpu_temperature():
    w = wmi.WMI(namespace="root\\wmi")
    temperature_info = w.MSAcpi_ThermalZoneTemperature()
    res = -1
    for temp in temperature_info:
        #t = temp.CurrentTemperature / 10.0 - 273.15
        t = temp.ActiveTripPoint[0] / 10.0 - 273.15
        print(temp, t)
        res = t
    return res

dt_now = datetime.datetime.now()

cpu_percent = psutil.cpu_percent(interval=1)
cpu_freq = psutil.cpu_freq().current
memory_info = psutil.virtual_memory()
cpu_temperature = get_cpu_temperature()

txt =  PC_NAME + ' ' + dt_now.strftime('%Y/%m/%d %H:%M:%S') + '\n'
txt += 'CPU: ' + str(cpu_percent) + ' % @ ' + str(cpu_freq / 1000) + ' GHz ' + str(round(cpu_temperature, 1)) + ' *C' + '\n'
txt += 'Mem: ' + str(round(memory_info.used / 1024 / 1024 / 1024, 1)) + ' GB ( ' + str(memory_info.percent) + ' % )' + '\n'
print(txt)

img = pyautogui.screenshot(IMG_FILE)

client = WebClient(token=TOKEN)

response = client.files_upload_v2(
    file=IMG_FILE,
    title=IMG_FILE,
    channels=[CHANNEL_ID],
    initial_comment=txt,
)
