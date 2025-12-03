import os
import VLCHandler

HOME = ""

def init():
    global HOME
    HOME = os.getcwd()

def backHome():
    os.chdir(HOME)

def getUsbDevices():
    output_stream = os.popen("lsblk")
    usbDevices = parseLsblkOutput(output_stream.readlines())
    usbDevices = [device for device in usbDevices if len(device["MOUNTPOINTS"])>0]
    displayOutputSring = "Dispositivi collegati:\n"
    displayOutputSring += "\n".join([str(x) + " - " + deviceInfoToString(i) for x , i in enumerate(usbDevices, 1)])
    displayOutputSring += "\nN.B. Partizioni diverse di uno stesso disco sono considerate come dischi diversi"
    #displayOutputSring = "\n".join([str(x) + " - " + i for x , i in enumerate(usbDevices,1)])
    #print(displayOutputSring)
    return usbDevices,displayOutputSring

def parseLsblkOutput(output):
    usbDevices = [{'NAME': 'omv', 'MAJ:MIN': '8:0', 'RM': '0', 'SIZE': '300.8G', 'RO': '0', 'TYPE': 'shared_folder', 'MOUNTPOINTS': '/app/Downloads'}]
    keys = [x.replace("\n","") for x in output[0].split(" ") if len(x)>0]
    for i in range(1,len(output)):
        deviceInfo = {}
        elementi = [x for x in output[i].split(" ") if len(x)>0]
        print("keys:\n",keys)
        print("elementi:\n",elementi)
        for j in range(len(keys)):
            try:
                deviceInfo[keys[j]] = elementi[j].replace("\n","")
            except IndexError:
                continue
        if deviceInfo.get("TYPE","") == "part":
            deviceInfo.get("NAME","") = deviceInfo.get("NAME","")[2:]
        if "mmcblk0" not in deviceInfo.get("NAME",""):
            usbDevices.append(deviceInfo)
        print(usbDevices)
    return usbDevices

def deviceInfoToString(deviceInfo):
    return deviceInfo.get("NAME","") + " con uno spazio totale di memoria di " + deviceInfo.get("SIZE","")

def deviceSelection(usbDevices,selection):
    deviceInfo = usbDevices[selection]
    os.chdir(deviceInfo.get("MOUNTPOINT",""))
    return displayMedia()
    print("Digita il nome del file che vuoi riprodurre, o forse vuoi esplorare le altre cartelle?")
    sceltaMedia(media)

def getMedia():
    cartelle, file = list(os.walk(os.getcwd()))[0][1:]
    media = [x for x in file if isMedia(x)]
    return media

def isMedia(file):
    permessi=["mp4","mp3","mkv"]
    return file.split(".")[-1] in permessi

def displayMedia():
    media = getMedia()
    displayOutputSring = "Media presenti:\n"
    displayOutputSring += "\n".join([str(x) + " - " + i for x , i in enumerate(media,1)])
    #print(displayOutputSring)
    return displayOutputSring, media

def sceltaMedia(media,scelta):
    #scelta = input()
    #print(scelta)
    #print(scelta in media)
    
    if scelta == "Esplora":
        esplora()
    elif scelta in media or scelta in [x.split(".")[0] for x in media]:
        VLCHandler.setMedia(scelta)
    else:
        print("Errore")
        #print("Scusami ma non ho capito cosa vuoi riprodurre.\nRiprova")
        #sceltaMedia(media)

def esplora():
    cartelle, file = list(os.walk(os.getcwd()))[0][1:]
    displayOutputSring = "Cartelle presenti:\n"
    displayOutputSring += "\n".join([str(x) + " - " + i for x , i in enumerate(cartelle,1)])
    #print(displayOutputSring)
    return displayOutputSring, cartelle

def isMountpoint(path):
    pathList = [x["MOUNTPOINT"] for x in getUsbDevices()[0]]
    return os.path.normpath(path) in (os.path.normpath(p) for p in pathList)
