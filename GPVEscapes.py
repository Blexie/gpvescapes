import xml.etree.ElementTree as ET
import ctypes
import tkinter
import sys
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
        if lap.get('twrr') == '1.000' and lap.get('pit') != '1' and lap.get('num') != driver.find('Laps').text:
            print(lap.get('num'))
            print(name.text)
            ctypes.windll.user32.MessageBoxW(0, name.text + ": Possible escape lap " + lap.get('num')
                                             + ". Please verify on the replay.", "Suspicious Lap")
        else:
            continue

ctypes.windll.user32.MessageBoxW(0, "Check complete!", "GPV Escape Check")
