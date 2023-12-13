import subprocess

class smart_dict(dict):
    def __missing__(self, key):
        return key

class dispositivo:
    def __init__(self, device_id):
        self.device_id = device_id
    
    commands = smart_dict()
    commands.update({
        "power on" : "on {id}",
        "power off" : "standby {id}",
        "go on pi" : "as",
        "power status" : "pow {id}",
        "name" : "name {id}",
        "device list" : "scan",
        "volume up" : "volup",
        "volume down" : "voldown",
        "mute" : "mute",
        "refresh connection" : "r",
    })

    execute = lambda self,command: subprocess.run("echo '{0}' | cec-client -s -d 1".format(str(self.commands[command]).format(id=self.device_id)), shell=True)

    power_on  = lambda self: self.execute("power on")
    power_off = lambda self: self.execute("power off")
    go_on_pi = lambda self: self.execute("go on pi")
    power_status = lambda self: self.execute("power status")
    name = lambda self: self.execute("name")
    device_list = lambda self: self.execute("device list")
    volume_up = lambda self: self.execute("volume up")
    volume_down = lambda self: self.execute("volume down")
    mute = lambda self: self.execute("mute")
    refresh_connection = lambda self: self.execute("refresh connection")

    test = lambda self,command: print(str(self.commands[command]).format(id=self.device_id))


"""
    
[tx] {bytes}              transfer bytes over the CEC line.
[txn] {bytes}             transfer bytes but don't wait for transmission ACK.
[on] {address}            power on the device with the given logical address.
[standby] {address}       put the device with the given address in standby mode.
[la] {logical address}    change the logical address of the CEC adapter.
[p] {device} {port}       change the HDMI port number of the CEC adapter.
[pa] {physical address}   change the physical address of the CEC adapter.
[as]                      make the CEC adapter the active source.
[is]                      mark the CEC adapter as inactive source.
[osd] {addr} {string}     set OSD message on the specified device.
[ver] {addr}              get the CEC version of the specified device.
[ven] {addr}              get the vendor ID of the specified device.
[lang] {addr}             get the menu language of the specified device.
[pow] {addr}              get the power status of the specified device.
[name] {addr}             get the OSD name of the specified device.
[poll] {addr}             poll the specified device.
[lad]                     lists active devices on the bus
[ad] {addr}               checks whether the specified device is active.
[at] {type}               checks whether the specified device type is active.
[sp] {addr}               makes the specified physical address active.
[spl] {addr}              makes the specified logical address active.
[volup]                   send a volume up command to the amp if present
[voldown]                 send a volume down command to the amp if present
[mute]                    send a mute/unmute command to the amp if present
[self]                    show the list of addresses controlled by libCEC
[scan]                    scan the CEC bus and display device info
[mon] {1|0}               enable or disable CEC bus monitoring.
[log] {1 - 31}            change the log level. see cectypes.h for values.
[ping]                    send a ping command to the CEC adapter.
[bl]                      to let the adapter enter the bootloader, to upgrade
                          the flash rom.
[r]                       reconnect to the CEC adapter.
[h] or [help]             show this help.
[q] or [quit]             to quit the CEC test client and switch off all
                          connected CEC devices.
    """
