import pymem as pm
import MemWork

mem , module_base = MemWork.getProcessAndModuleFromName("Stardew Valley.exe","coreclr.dll")

time_staticOffset = 0x004AD958
time_offsets = [0x0, 0x80, 0x28, 0x318, 0x628]
time_adress = MemWork.createPointerAddr(mem,module_base,time_staticOffset,time_offsets)

time_adress = MemWork.createPointerAddr(mem,module_base,0x004AD958,[0x0, 0x80, 0x28, 0x318, 0x628])


mem.write_int(time_adress,930)