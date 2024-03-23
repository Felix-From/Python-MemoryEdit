import pymem as pm
import MemWork


#init

mem , module_base = MemWork.getProcessAndModuleFromName("Stardew Valley.exe","coreclr.dll")

#Freeze Example

stamina_address = MemWork.createPointerAddr(mem,module_base,0x004A43A8,[0x1E8,0x40,0xA8,0xB8C,0x10,0x370,0x9DC])

MemWork.createPointerFreezer(mem,stamina_address,260.0,"float")

MemWork.triggerPointerFreezer(stamina_address,True)

#LookUp Example

def __callbackFunction(triggerValue,itemValue):
    print("Test done from Trigger: "+ str(triggerValue)+ " Value changed to :" + str(itemValue))
    return

stamina_address = MemWork.createPointerAddr(mem,module_base,0x004A43A8,[0x1E8,0x40,0xA8,0xB8C,0x10,0x370,0x9DC])

_type = "int"
AnzeigeName = "Stamina"
#__callbackFunction function to call back if value changed
triggerValue = 5 
lastRead = 270.0 #Last read (unset = -1)

MemWork.createLookUpAddress(mem,stamina_address,_type,AnzeigeName,__callbackFunction,triggerValue,lastRead)
MemWork.triggerLookUpAddress(stamina_address,True)

#Keep alive
while True:
    pass
