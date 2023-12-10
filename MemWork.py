import pymem
from pymem.process import module_from_name
import threading as Thread

def __dprint(stuff_to_print,loop = None):
    global debug
    if debug:
        if (debug_freezeloop and loop == 1) or (debug_lookUploop and loop == 2) or loop is None:
            print(stuff_to_print)
    return stuff_to_print

#Process und Module Stuff

def getProcessAndModuleFromName(ProcessName,moduleName): #Returns Process , module !! erwarte auch 2 variabeln mit z.B. process,module_base = getProcessAndModuleFromName("Stardew Valley.exe","coreclr.dll")
    mem = pymem.Pymem(ProcessName)
    module_base = module_from_name(mem.process_handle, ""+moduleName).lpBaseOfDll
    return mem, module_base

# Pointer Stuff

def __getPtrAddr(process, address, offsets):
    global debug
    try:
        addr = process.read_longlong(address)
        __dprint(f"Initial Address: 0x{addr}")
        for offset in offsets:
            if offset != offsets[-1]:
                addr = process.read_longlong(addr + offset)
                __dprint(f"Offset 0x{offset}: 0x{addr}")
        addr = addr + offsets[-1]
        __dprint(f"Final Address: 0x{addr}")
        return addr
    except pymem.exception.MemoryReadError as e:
        print(f"@@@@@@@@@@ Error reading memory at address: {e} @@@@@@@@@@@@")
        return None

def createPointerAddr(process,module_base,StaticOffset,Offsets):
    return __getPtrAddr(process,module_base+StaticOffset,Offsets)

#----------------------------------------------------------------------------------
#----------------------------------------------------------------------------------
#-----------Pointer Freezer
#----------------------------------------------------------------------------------
#----------------------------------------------------------------------------------
#   pointersToFreeze[i]             ArrayErklärung
# i=0   Process
#   1   Address 
#   2   Value - Freezewert
#   3   Valuetype - als str den typ z.B. "int"
#   4   state - active True/False
#   5   lastRead


def createPointerFreezer(process, address, value, valuetype, state=False):
    exist = any(pointer[1] == address for pointer in pointersToFreeze)
    if not exist:
        pointersToFreeze.append([process, address, value, valuetype, state, None])
                                                                            #None = lastRead
    return

def triggerPointerFreezer(address,state,value=None,valuetype=None):
    #Trigger True/False je nach state, aber man kann auch value und valuetype anpassen lassen.
    __dprint("triggerPointerFreezer | "+str(address)+"|"+str(state))
    for pointer in pointersToFreeze:
        if pointer[1] == address: # Wenn es einen eintrag findet mit der Adresse
            __dprint("triggerFreeze Pointer Found.")
            if value is not None: # Wenn gesetzt dann setzt er die die Value auf Value
                pointer[2] = value
            if valuetype is not None: #gleiche wie oben
                pointer[3] = valuetype
            pointer[4] = state #state True/False ob es gefreezed sein soll oder nicht
            pointer[5] = None  #lastRead
            break
    return

def removePointerFreezer(address):
    callback = False
    for pointer in pointersToFreeze:
        if pointer[1] == address:
            __dprint("Removed PointerFreezer "+hex(address))
            pointersToFreeze.remove(pointer)
            break
    return callback

def __freezeLoop():
    global pointersToFreeze
    while True:
        if pointersToFreeze != []:
            for pointer in pointersToFreeze:
                if pointer[4]: #Is active?
                    try:
                        if pointer[0].read_int(pointer[1]) != pointer[5]:
                            __dprint("Freezeloop Pointer Write für "+hex(pointer[1])+" Value:"+str(pointer[2]),1)
                            match pointer[3]:
                                case "int":
                                    pointer[0].write_int(pointer[1],pointer[2])
                                    pointer[5] = pointer[2]
                                    __dprint("Freezeloop write int",1)
                                case "float":
                                    pointer[0].write_float(pointer[1],pointer[2])
                                    pointer[5] = pointer[2]
                                    __dprint("Freezelóop write float",1)
                                case "string":
                                    pointer[0].write_string(pointer[1],pointer[2])
                                    pointer[5] = pointer[2]
                                    __dprint("Freezeloop write string",1)
                                case "bytes":
                                    pointer[0].write_bytes(pointer[1],pointer[2],4)
                                    pointer[5] = pointer[2]
                                    __dprint("Freezeloop write bytes",1)
                    except pymem.exception.MemoryReadError as e:
                        print(f"@@@@@@@@@@ [FreezerPointer] Error reading memory at address: {e} @@@@@@@@@@@@")
                        return None
    return

#----------------------------------------------------------------------------------
#----------------------------------------------------------------------------------
#-----------LookUp - Change -
#----------------------------------------------------------------------------------
#----------------------------------------------------------------------------------
#   pointersToLookUp[i]             ArrayErklärung
# i=0   process
#   1   address
#   2   type
#   3   triggerName (Print bei Trigger)
#   4   triggerFunction (pointer)
#   5   triggerValue (id oder so für selbst benutzung.)
#   6   lastRead - Letzer Wert seit veränderung.
#   7   triggerState - active True/False

def createLookUpAddress(process,address,type,triggerName,triggerFunction,triggerValue, lastRead=-1,triggerState = False):
    exist = any(pointer[1] == address for pointer in pointersToLookUp)
    if not exist:
        pointersToLookUp.append([process,address,type,triggerName,triggerFunction,triggerValue, lastRead,triggerState])
    return

def triggerLookUpAddress(address,state,resetLastRead = False):
    #Trigger True/False je nach state.
    __dprint("triggerLookUpAdress | "+str(address)+"|"+str(state))
    for pointer in pointersToLookUp:
        if pointer[1] == address: # Wenn es einen eintrag findet mit der Adresse
            __dprint("triggerLookUpAddress Pointer Found.")
            pointer[7] = state
            if resetLastRead:
                pointer[6] = 0
            break
    return

def removeLookUpAddress(address):
    for pointer in pointersToLookUp:
        if pointer[1] == address:
            __dprint("Removed lookUpAddress "+hex(address))
            pointersToLookUp.remove(pointer)
            break

def __onTriggerLookUp(pointer):
    __dprint("onTriggerLookUp! Found! -> "+str(pointer[3]))
    match pointer[2]:
        case "int":
            pointer[4](pointer[5],pointer[0].read_int(pointer[1]))
        case "float":
            pointer[4](pointer[5],pointer[0].read_float(pointer[1]))
        case "bytes":
            pointer[4](pointer[5],int.from_bytes(pointer[0].read_bytes(pointer[1],4)))
        case "string":
            pointer[4](pointer[5],pointer[0].read_string(pointer[1]))
    return

def __lookUpLoop():
    while True:
        for pointer in pointersToLookUp:
            if pointer[7]:
                try:
                    match pointer[2]:
                        case "int":
                            if pointer[0].read_int(pointer[1]) != pointer[6]:
                                debug_print_Text = "LookUpPool "+hex(pointer[1])+" read new value! Old: "+str(pointer[6])+" | New:"
                                pointer[6] = pointer[0].read_int(pointer[1])
                                __dprint(debug_print_Text+str(pointer[6]),2)
                                __onTriggerLookUp(pointer)
                        case "float":
                            if pointer[0].read_float(pointer[1]) != pointer[6]:
                                debug_print_Text = "LookUpPool "+hex(pointer[1])+" read new value! Old: "+str(pointer[6])+" | New:"
                                pointer[6] = pointer[0].read_float(pointer[1])
                                __dprint(debug_print_Text+str(pointer[6]),2)
                                __onTriggerLookUp(pointer)
                        case "bytes":
                            if int.from_bytes(pointer[0].read_bytes(pointer[1],4)) != pointer[6]:
                                debug_print_Text = "LookUpPool "+hex(pointer[1])+" read new value! Old: "+str(pointer[6])+" | New:"
                                pointer[6] = int.from_bytes(pointer[0].read_bytes(pointer[1],4))
                                __dprint(debug_print_Text+str(pointer[6]),2)
                                __onTriggerLookUp(pointer)
                        case "string":
                            if pointer[0].read_string(pointer[1]) != pointer[6]:
                                debug_print_Text = "LookUpPool "+hex(pointer[1])+" read new value! Old: "+str(pointer[6])+" | New:"
                                pointer[6] = pointer[0].read_string(pointer[1])
                                __dprint(debug_print_Text+str(pointer[6]),2)
                                __onTriggerLookUp(pointer)
                except pymem.exception.MemoryReadError as e:
                    print(f"@@@@@@@@@@ [FreezerPointer] Error reading memory at address: {e} @@@@@@@@@@@@")
                    return None
                pass
        pass

#----------------------------------------------------------------------------------
#----------------------------------------------------------------------------------
#-----------Multithreading
#----------------------------------------------------------------------------------
#----------------------------------------------------------------------------------

def __startFreezeLoop():
    freezeThread = Thread.Thread(target = __freezeLoop)
    freezeThread.daemon = True #Damit die Threads mit zu gehen wenn man das Programm schließt
    freezeThread.start()
    return freezeThread

def __startLookUpLoop():
    loopUpThread = Thread.Thread(target = __lookUpLoop)
    loopUpThread.daemon = True # Ohne das würden die Threads einfach offen bleiben und ram fressen.
    loopUpThread.start()
    return loopUpThread

#----------------------------------------------------------------------------------
#----------------------------------------------------------------------------------
#-----------Debug Zone.
#----------------------------------------------------------------------------------
#----------------------------------------------------------------------------------

debug = True
debug_freezeloop = False
debug_lookUploop = True


#----------------------------------------------------------------------------------
#----------------------------------------------------------------------------------
#-----------Main init.
#----------------------------------------------------------------------------------
#----------------------------------------------------------------------------------

pointersToFreeze = []
freezeThread = __startFreezeLoop()
pointersToLookUp = []
loopUpThread = __startLookUpLoop()
