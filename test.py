import pymem as pm
import MemWork

#-----------------------------------------------------------
# MemWork Basic Pointer
mem , module_base = MemWork.getProcessAndModuleFromName("Stardew Valley.exe","coreclr.dll")

#time_staticOffset = 0x004AD958
#time_offsets = [0x0, 0x80, 0x28, 0x318, 0x628]
#time_adress = MemWork.createPointerAddr(mem,module_base,time_staticOffset,time_offsets)
    # oder als one liner
#time_adress = MemWork.createPointerAddr(mem,module_base,0x004AD958,[0x0, 0x80, 0x28, 0x318, 0x628])

#-----------------------------------------------------------
# Memwork Freeze Pointer

    # Stamina_adress wie normal erstellen
stamina_address = MemWork.createPointerAddr(mem,module_base,0x004A43A8,[0x1E8,0x40,0xA8,0xB8C,0x10,0x370,0x9DC])
    # Zum erstellen des PinterFreezers ein mal ausführen mit den Daten
MemWork.createPointerFreezer(mem,stamina_address,260.0,"float")
    # Zum ändern des Triggerzustandes oder der Value/Valuetype  Value/Valuetype kann leer gelassen werden wenn nichts verändert wird.
MemWork.triggerPointerFreezer(stamina_address,True)
#MemWork.triggerPointerFreezer(stamina_address,False,10,"int")

#-----------------------------------------------------------

#Memwork LookUp Pointer

    #Funktion erstellen die bei Veränderung getriggert werden soll
    #Wichtig 2 Parameter, hier: traiggerValue, itemValue (name egal)
    #Wenn der Trigger hier ankommt steht in triggerValue eine selbst ausgesuchte 
    #triggerValue(falls man 1 callback für mehrere pointer benutzt zum zuordnen)
    #Und in itemValue steht der veränderte wert.
def __callbackFunction(triggerValue,itemValue):
    print("Test bestanden | "+ str(triggerValue)+ " | " + str(itemValue))
    return

    # Stamina_adress wie normal erstellen
stamina_address = MemWork.createPointerAddr(mem,module_base,0x004A43A8,[0x1E8,0x40,0xA8,0xB8C,0x10,0x370,0x9DC])

    #createLookUpAddress process,address,type(als str),"AnzeigeName",Callback Function, triggerValue , startwert (ohne angabe = -1)
_type = "int" # muss als Str sein.
AnzeigeName = "Angeln" #Wird beim OnTriggerLookUP in Console geschrieben
#__callbackFunction die Funktion die es ausrufen soll wenn der wert sich ändert.
triggerValue = 5 #Ein von dir zugewiesener Text der beim callback als erste Variable wieder raus gegeben wird ( zur zuweisung oder so)
lastRead = 270.0 #Der Wert mit dem er starten soll, wenn weg gelassen wird ist er -1
#Aber Achtung, bei -1 wird er zu 100% min. 1 mal triggern nach erstellung.(Wenn er Aktiv getriggert wird das erste mal)
MemWork.createLookUpAddress(mem,0x1F7022083A4,_type,AnzeigeName,__callbackFunction,triggerValue,lastRead)
#vergleicht den lastRead mit aktuell und wenn es nicht so ist triggert er deine Funktion
#und speichert den neuen wert in lastRead damit er nicht 2x los geht.
MemWork.triggerLookUpAddress(0x1F7022083A4,True)

def debug_func():
    MemWork.triggerPointerFreezer(stamina_address,False)
    MemWork.triggerLookUpAddress(0x1F7022083A4,False)

    print(str(MemWork.pointersToFreeze[0]))
    print(str(MemWork.pointersToLookUp[0]))

    MemWork.removePointerFreezer(stamina_address)
    MemWork.removeLookUpAddress(0x1F7022083A4)

    print(str(MemWork.pointersToFreeze))
    print(str(MemWork.pointersToLookUp))
    return

import keyboard
keyboard.on_release_key("F1",lambda _:debug_func())

#Damit das Programm laufen bleibt.
while True:
    pass