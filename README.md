# Private Python version of CheatEngine. Tested on Stardew Valley.
This respository was used for version control.\n

MemWork.py can be imported in your local script and can be used. 

main.py is with an Example on how to use it.

(comments/Descriptions are written in german... sorry)

main-lite.py is a simpler version with some English comments<br/>

>**Requirements**:<br/>
>pip install pymem

# Functions MemWork:
## Process und Module Stuff
**Function:** getProcessAndModuleFromName(ProcessName,moduleName)

**Returns:** process, module_base


## Pointer Stuff
**Function:** createPointerAddr(process,module_base,StaticOffset,Offsets)

**Returns:** Calculated_Address

**Infos:** to find the StaticOffset and Offsets[] you need to use CheatEngine or something like that and do a Pointerscan.<br/>
If you do that you also will know what module_base you need.

## Pointer Freezer
## Description
>----------------------------------------------------------------------------------
>Pointer Freezer
>----------------------------------------------------------------------------------
>   pointersToFreeze[i] Array<br/>
> i=0   Process<br/>
>   1   Address <br/>
>   2   Value - Freezevalue <br/>
>   3   Valuetype - as string typename like "int"<br/>
>   4   state - active True/False<br/>
>   5   lastRead<br/>

## Functions:
**Function:** createPointerFreezer(process, address, value, valuetype, state=False)

**Returns:** none



**Function:** triggerPointerFreezer(address,state,value=None,valuetype=None)

**Returns:** none



**Function:** removePointerFreezer(address)

**Return:** always false == looks like i planed it to return true if it removes something but i forgot it :x .



## LookUp Pointer
## Description
>----------------------------------------------------------------------------------
> LookUp Pointer for changes
>----------------------------------------------------------------------------------
>   pointersToLookUp[i] Array<br/>
> i=0   process<br/>
>   1   address<br/>
>   2   type<br/>
>   3   triggerName (Print bei Trigger)<br/>
>   4   triggerFunction (pointer)<br/>
>   5   triggerValue (id oder so für selbst benutzung.)
>   6   lastRead - Letzer Wert seit veränderung.<br/>
>   7   triggerState - active True/False<br/>

## Functions:
**Function:** createLookUpAddress(process,address,type,triggerName,triggerFunction,triggerValue, lastRead=-1,triggerState = False)

**Returns:** none

**Function:** triggerLookUpAddress(address,state,resetLastRead = False)

**Returns:** none

**Function:** removeLookUpAddress(address)

**Returns:** none

## Debug Functions

Variables:

**debug** = True <--- Turns on Debugprints

**debug_freezeloop** = False <--- Turns on Debugprints for the FreezeLoop

**debug_lookUploop** = True <--- Turns on Debugprints for the lookUpLoop

<br/>
# Examples <br/>
**main.py** but it has **German** comments<br/>
To understand the functions without comments look into **main-lite.py**<br/>
