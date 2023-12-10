from pymem import *
from pymem.process import module_from_name
import keyboard

#Debug

def printh(string): # Printet etwas in die Konsole aber in Hex und gibt den Hex wert als Return weiter. (gut um nach einer rechung ein debug einzubauen)
    print(hex(string))
    return hex(string)


# Pointer
def getPtrAddr(address, offsets):
    try:
        addr = mem.read_longlong(address)
        print(f"Initial Address: 0x{addr}")
        for offset in offsets:
            if offset != offsets[-1]:
                addr = mem.read_longlong(addr + offset)
                print(f"Offset 0x{offset}: 0x{addr}")
        addr = addr + offsets[-1]
        print(f"Final Address: 0x{addr}")
        return addr
    except pymem.exception.MemoryReadError as e:
        print(f"Error reading memory at address: {e}")
        return None
    
def createPointerAddr(StaticOffset,Offsets):
    global game_module
    return getPtrAddr(game_module+StaticOffset,Offsets)

def checkIfAdressWorks(adress):
    if (adress and adress != ""): 
        return True
    return False
#Hi
#Keybinds
def addKeyBind(keyName,keyFunktionName,description,doCheck = True):
    #KeyName = "F1" , keyFunktionName = "Heal" , desc. = "Heilt dich" , doCheck = True/False
    #doCheck ist normal auf True aber man kann mit False den Duplicate check umgehen.
    if doCheck:
        if keyName not in hotkeys and keyFunktionName not in hotkeyFunktionNames:
            hotkeys.append(keyName)
            hotkeyFunktionNames.append(keyFunktionName)
            hotkeyDesc.append(description)
            keyboard.on_release_key(keyName, lambda _:toggleKey(keyFunktionName))
        else:
            raise Exception("ERROR - addKeyBind - Key existiert schon")
        return 
    else:
        hotkeys.append(keyName)
        hotkeyFunktionNames.append(keyFunktionName)
        hotkeyDesc.append(description)
        keyboard.on_release_key(keyName, lambda _:toggleKey(keyFunktionName))
    return

def toggleKey(keyFunktionName):
    global lock_hp,lock_stamina,lock_time
    log_message = "Key "+keyFunktionName+" wurde getriggert!"
    match keyFunktionName:
        case'HP_Toggle':
            lock_hp = not lock_hp
            log_message = log_message + "State: "+ str(lock_hp)
        case'Stamina_Toggle':
            lock_stamina = not lock_stamina
            log_message = log_message + "State: "+ str(lock_stamina)
        case'Time_Toggle':
            lock_time = not lock_time
            log_message = log_message + "State: "+ str(lock_time)
        case'Money_Add':
            current = mem.read_int(money_address)
            mem.write_int(money_address,current +1000)
            log_message = log_message + "Davor: "+str(current)+"$ | Bekommen +"+str(1000)+"$."
        case'Debug': # Ist wie ein kleines Wiki, falls ich mal was vergesse
            #debug_pointerAddress = createPointerAddr(0xFFFFFFFF,[0xFFF,0xFFF,0xFFF,0xFFF,0xFFF,0xFFF]) # KEIN ECHTER POINTER
            #print(mem.read_int(debug_pointerAddress)) # Printet es normal | Ließt die Adresse aus errechnetem Pointer
            #printh(mem.read_int(debug_pointerAddress)) # Printet es als Hex | Same
            #anzahl = 50
            #mem.write_int(debug_pointerAddress,anzahl) # Setzt werte vom debug pointer auf anzahl
            #anzahl = int.from_bytes(mem.read_bytes(debug_pointerAddress,length=4)) # Falls du mal ein 4 Byte int auslesen musst convertiert es gleich zu int.
            #mem.write_bytes(debug_pointerAddress,(4).to_bytes(4,byteorder = 'big')) # Oder byteorder = 'little' hab ich noch nicht gebraucht.
            pass       
    print(log_message)
    return

#Main Start
mem = Pymem("Stardew Valley.exe")
game_module = module_from_name(mem.process_handle, "coreclr.dll").lpBaseOfDll

#HotKey Locks
lock_hp = False
lock_stamina = False
lock_time = False

#Hotkeys Arrays
hotkeyFunktionNames = []
hotkeyDesc = []
hotkeys = []

#Keybinds
addKeyBind("F1","HP_Toggle","Godmode.")
addKeyBind("F2","Stamina_Toggle","Unlimited Ausdauer.")
addKeyBind("F3","Time_Toggle", "Friert Zeit auf zwischen 10 und 12 ein.")
addKeyBind("F4","Money_Add", "Gibt dir 1000$.")
addKeyBind("F5","Debug","Benutze ich für tests.")

#Offsets
#Int
hp_address = createPointerAddr(0x004ADA80,[0x8, 0xD78, 0x18, 0x70, 0xC3C, 0x0, 0x6C4])

money_address = createPointerAddr(0x004A82C8, [0x318, 0xC8, 0x18, 0x40, 0x10, 0x3F0, 0x7C4])

time_address = createPointerAddr(0x004AD958, [0x0, 0x80, 0x28, 0x318, 0x628])
#Float
stamina_address = createPointerAddr(0x004A43A8,[0x1E8,0x40,0xA8,0xB8C,0x10,0x370,0x9DC])



#world

for i in range(len(hotkeys)):
    print("Hotkey ADD: Key = '"+hotkeys[i]+"' | KeyFunktionName ='"+hotkeyFunktionNames[i]+"' | Beschreibung = '"+hotkeyDesc[i]+"'")

mem.write_int(hp_address,mem.read_int(hp_address)) # Muss man irgendwie 1 mal machen.

#While True Schleife
while True:
    if not mem.check_wow64():
        #--Stats
        if(lock_hp):
            if (mem.read_int(hp_address)<=75):
                mem.write_int(hp_address,100)
        if(lock_stamina):
            if (mem.read_float(stamina_address)<=250.0):
                mem.write_float(stamina_address,270.0)
        #--World
        if(lock_time):
            if (mem.read_int(time_address)>=1200 or mem.read_int(time_address)<=950):
                mem.write_int(time_address,1000)
    else:
        raise Exception("Kein Stardew Valley offen!")

    

#Scrapyard

def beispiele():
    print("Davor: "+str(mem.read_int(hp_adress)))
    mem.write_int(hp_adress,99)
    print("Danach: "+str(mem.read_int(hp_adress)))

    print("Davor: "+str(mem.read_int(money_adress)))
    mem.write_int(money_adress,10000)
    print("Danach: "+str(mem.read_int(money_adress)))

    print("Davor: "+str(mem.read_int(time_adress)))
    mem.write_int(time_adress,950)
    print("Danach: "+str(mem.read_int(time_adress)))

    print("Davor: "+str(mem.read_float(stamina_adress)))
    mem.write_float(stamina_adress,269.0)
    print("Danach: "+str(mem.read_float(stamina_adress)))
    return 0
