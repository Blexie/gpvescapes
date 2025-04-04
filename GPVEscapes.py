import xml.etree.ElementTree as ET
import ctypes
import tkinter
import sys
import datetime
from tkinter import filedialog

tkroot = tkinter.Tk()
tkroot.overrideredirect(True)
tkroot.attributes("-alpha", 0)


def getqualifile():
    qualifile = filedialog.askopenfilename(filetypes=[("XML File", ".xml")], title="Select a QUALIFYING file")
    if not qualifile:
        sys.exit(2)
    else:
        qualitree = ET.parse(qualifile)
        qualiroot = qualitree.getroot()
        return qualiroot


qualiroot = getqualifile()
for driver in qualiroot.iter('Driver'):
    name = driver.find('Name')
    for lap in driver.findall('Lap'):
        if lap.get('twrr') == '1.000' and lap.get('pit') != '1' and lap.get('num') != driver.find('Laps').text and lap.get('et') != "--.---":
            for nextlap in driver.findall('Lap'):
                if int(nextlap.get('num')) == int(lap.get('num')) + 1:
                    timestamp = str(datetime.timedelta(seconds=round(float(nextlap.get('et')))))
                    break
            ctypes.windll.user32.MessageBoxW(0, name.text + ": Possible escape lap " + lap.get('num')
                                             + " (Approx: "+ timestamp + ")" + '\n' + "Please verify on the replay."
                                             , "Suspicious Lap")
        else:
            continue

ctypes.windll.user32.MessageBoxW(0, "Check complete!", "GPV Escape Check")
