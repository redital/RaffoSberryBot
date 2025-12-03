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
    usbDevices = []
    keys = [x.replace("\n","") for x in output[0].split(" ") if len(x)>0]
    for i in range(1,len(output)):
        deviceInfo = {}
        elementi = [x for x in output[i].split(" ") if len(x)>0]
        print(elementi)
        for j in range(len(keys)):
            deviceInfo[keys[j]] = elementi[j].replace("\n","")
        if deviceInfo["TYPE"] == "part":
            deviceInfo["NAME"] = deviceInfo["NAME"][2:]
        if "mmcblk0" not in deviceInfo["NAME"]:
            usbDevices.append(deviceInfo)
    
    return usbDevices

def deviceInfoToString(deviceInfo):
    return deviceInfo["NAME"] + " con uno spazio totale di memoria di " + deviceInfo["SIZE"]

def deviceSelection(usbDevices,selection):
    deviceInfo = usbDevices[selection]
    os.chdir(deviceInfo["MOUNTPOINT"])
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
