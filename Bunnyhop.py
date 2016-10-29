'''
INSTRUCTIONS:
bind f7 "+jump 32;-jump 32"
unbind space

NOTES:
SendMessage works but feels worse to me, so I'm using keybd_event.
Both work, however, so feel free to try one or the other.
'''
from ctypes import *
from time import sleep

OpenProcess = windll.kernel32.OpenProcess
ReadProcessMemory = windll.kernel32.ReadProcessMemory
WriteProcessMemory = windll.kernel32.WriteProcessMemory
CreateToolhelp32Snapshot = windll.kernel32.CreateToolhelp32Snapshot
Process32First = windll.kernel32.Process32First
Process32Next = windll.kernel32.Process32Next
Module32First = windll.kernel32.Module32First
Module32Next = windll.kernel32.Module32Next
CloseHandle = windll.kernel32.CloseHandle
GetAsyncKeyState = windll.User32.GetAsyncKeyState
SendMessage = windll.User32.SendMessageA
keybd_event = windll.User32.keybd_event
FindWindow = windll.User32.FindWindowA


class PROCESSENTRY32(Structure):
_fields_ = [("dwSize", c_ulong),("cntUsage", c_ulong),("th32ProcessID", c_ulong),("th32DefaultHeapID", c_ulong),("th32ModuleID", c_ulong),("cntThreads", c_ulong),("th32ParentProcessID", c_ulong),("pcPriClassBase", c_ulong),("dwFlags", c_ulong),("szExeFile", c_char * 260)]
class MODULEENTRY32(Structure):
_fields_ = [( 'dwSize' , c_ulong ) , ( 'th32ModuleID' , c_ulong ),( 'th32ProcessID' , c_ulong ),( 'GlblcntUsage' , c_ulong ),( 'ProccntUsage' , c_ulong ) ,( 'modBaseAddr' , c_void_p ) ,( 'modBaseSize' , c_ulong ) , ( 'hModule' , c_void_p ) ,( 'szModule' , c_char * 256 ),( 'szExePath' , c_char * 260 ) ]


# Get a processID by the name of the process
def GetPIDByName(ProcessName):
hProcessSnap = CreateToolhelp32Snapshot(0x00000002, 0)
pe32 = PROCESSENTRY32()
pe32.dwSize = sizeof(PROCESSENTRY32)
Process32First(hProcessSnap, byref(pe32))
pid = None
while True:
if (pe32.szExeFile.lower()==ProcessName.lower()):
pid=pe32.th32ProcessID
break
if not Process32Next(hProcessSnap, byref(pe32)):
break
CloseHandle(hProcessSnap)
return pid

# Get the base address of a loaded module
def GetModuleBase(PID,ModuleName):
hModuleSnap = CreateToolhelp32Snapshot( 0x00000008, PID );
me32 = MODULEENTRY32()
me32.dwSize = sizeof(MODULEENTRY32)
Module32First( hModuleSnap, byref(me32))
base = None
while True:
if (me32.szModule.lower()==ModuleName.lower()):
base=me32.modBaseAddr
break
if not Module32Next(hModuleSnap, byref(me32)):
break
CloseHandle(hModuleSnap)
return base

ProcID = GetPIDByName('hl2.exe')
EngineBase = GetModuleBase(ProcID,'engine.dll')
ClientBase = GetModuleBase(ProcID,'client.dll')
ProcHandle = OpenProcess(0x1FFFFF,0,ProcID)
ProcHWND = FindWindow('Valve001',0)
onGroundAddr = ClientBase+0x782158 

print ProcID,EngineBase,ClientBase,ProcHandle,ProcHWND

bytesRead = c_uint()
onGround = c_ulong()
while True:
sleep(.001)
ReadProcessMemory(ProcHandle,c_void_p(onGroundAddr ),byref(onGround),4,byref(bytesRead))
if (not onGround.value == 4294967295) and (GetAsyncKeyState(32)&0x80000000):
keybd_event(0x76,0x41,0,0)
keybd_event(0x76,0x41,2,0)
#SendMessage(ProcHWND, 0x0100, 0x76, 0x410000);
#SendMessage(ProcHWND, 0x0101, 0x76, 0x410000);
