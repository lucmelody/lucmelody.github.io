#include "ProcMem.h"
#include <conio.h>

ProcMem mem;
using namespace std;

class read; //Definition
class read{
public:
       
    int i_Enemies[32]; //Enemy Array
    int i_Count; //Found Counter / Array Index - Allows Us To Populate Enemy Array Correctly (in order)
    int i_team;
    int e_team;
    DWORD dwClient;
    DWORD dwPBase;
    DWORD dwEntity;

    void Read()
    {
        dwClient = mem.Module("client.dll");
        dwPBase = mem.Read<DWORD>(dwClient + 0xA33234);
        i_team = mem.Read<int>(dwPBase + 0xF0);

        for(int i = 0; i < 64; i++)
        {
            //Loop From Base Entity Address by 0x10 On Each Iteration
            dwEntity = mem.Read<DWORD>((dwClient + 0xA4C3E4) + (i * 0x10));

            //Prevent Crash From Reading Null Pointer - also stop counting when weve read the last entity
            if(!dwEntity)
                continue;

            e_team = mem.Read<int>(dwEntity + 0xF0);

            //If An Enemy Has Been Found, Store Their Entity Index ID Inside Array
            if(e_team != i_team && e_team > 1)
            {
                i_Enemies[i_Count] = mem.Read<int>(dwEntity + 0x64);
                i_Count++;
            }
        }
    }
}info;

void Trigger()
{
    //Variables
    int iTarList[32]; //Enemy Array
    int iResponse = 1; //Default Fire Rate
    int * i_cID;
    int cID;

    //Read Relevant info
    info.Read();

    while(1)
    {
        //Read Relevant info
        info.Read();
     
        //Populate Enemy Array
        for(int i = 0; i < info.i_Count; i++)    
            iTarList[i] = info.i_Enemies[i];    
             
        //Read Whats In Crosshair
        cID = mem.Read<int>(info.dwPBase + 0x2374);

        //Compare Current ID To Enemy Arra
        i_cID = find(iTarList, iTarList + info.i_Count, cID);

        //Shoot If Current ID Matches Enemy ID
        while(*i_cID == cID)
        {       
            //Read Whats In Crosshair
            cID = mem.Read<int>(info.dwPBase + 0x2374);

            //Compare Current ID To Enemy Arra
            i_cID = find(iTarList, iTarList + info.i_Count, cID);

            //Less Detectable Method
            mouse_event( MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0 );
            Sleep(iResponse);
            mouse_event( MOUSEEVENTF_LEFTUP, 0, 0, 0, 0 );
                 
            //End Triggerbot - Safety Key Encase Of Infinite Loop
            if(GetAsyncKeyState(VK_END)&1)
                return;
        }

        //Reset Entity Counter
        info.i_Count = 0;

#pragma region Fire Rate Modifier

        if(GetAsyncKeyState(VK_ADD)&1)
        {
            iResponse++;
            if(iResponse > 15)
                iResponse = 15;

            system("cls");
            _cprintf("%d", iResponse);
        }

        if(GetAsyncKeyState(VK_SUBTRACT)&1)
        {
            iResponse--;
            if(iResponse < 1)
                iResponse = 1;

            system("cls");
            _cprintf("%d", iResponse);
        }

#pragma endregion

        //End Triggerbot
        if(GetAsyncKeyState(VK_END)&1)
            break;
    }   
}


int main()
{
    mem.GetProcess("csgo.exe");

    while(1)
    {
        if(GetAsyncKeyState(VK_HOME))
        {
            cout << "\nON";
            Trigger();  
            cout << "\nOFF";
        }
    }
    return 0;
}
    
