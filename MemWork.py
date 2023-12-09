from pymem import *
from pymem.process import module_from_name

#Process und Module Stuff

def getProcessAndModuleFromName(ProcessName,moduleName): #Returns Process , module !! erwarte auch 2 variabeln mit z.B. process,module_base = getProcessAndModuleFromName("Stardew Valley.exe","coreclr.dll")
    mem = pymem.Pymem(ProcessName)
    module_base = module_from_name(mem.process_handle, ""+moduleName).lpBaseOfDll
    return mem, module_base

# Pointer Stuff

def __getPtrAddr(process, address, offsets, debug=False):
    try:
        addr = process.read_longlong(address)
        if debug:
            print(f"Initial Address: 0x{addr}")
        for offset in offsets:
            if offset != offsets[-1]:
                addr = process.read_longlong(addr + offset)
                if debug:
                    print(f"Offset 0x{offset}: 0x{addr}")
        addr = addr + offsets[-1]
        if debug:
            print(f"Final Address: 0x{addr}")
        return addr
    except pymem.exception.MemoryReadError as e:
        print(f"@@@@@@@@@@ Error reading memory at address: {e} @@@@@@@@@@@@")
        return None

def createPointerAddr(process,module_base,StaticOffset,Offsets,debug = False):
    return __getPtrAddr(process,module_base+StaticOffset,Offsets,debug)