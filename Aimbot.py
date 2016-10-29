PLAYER_DATA GetMyPlayerData(void)
PLAYER_DATA GetPlayerData(BYTE PlayerNumber)
typedef struct _PLAYER_DATA {
DWORD baseadd; // base address of this current player
DWORD coordEW; // East/West (X) co-ord
DWORD coordNS; // North/South (Y) co-ord
DWORD coordUD; // Up/Down (Z) co-ord
DWORD coordEWa; // The address of the players EW co-ord
DWORD coordNSa; // The address of the players NS co-ord
DWORD coordUDa; // The address of the players UD (up/down..wth was i thinking when naming this) co-ord
DWORD lookX; // The players X-axis look (what will change if you move the mouse side to side)
DWORD lookY; // The players Y-axis look (what will change if you move the mouse forwards and backwards)
DWORD lookXa; // The address of the X look
DWORD lookYa; // The address of the Y look
char name; // Holds the current players name
DWORD namea; // The address of the current players name
} PLAYER_DATA;
Code:
#define mBase 0xBD63D8
#define hBase 0xB0D228
///
PLAYER_DATA GetMyPlayerData(void)
{
PLAYER_DATA Player; // Create a blank PLAYER_DATA struct
ZeroMemory(&Player, sizeof(PLAYER_DATA)); // Initiate it all to 0 (thanks L.Spiro, this solved some problems)
Peek((void*)mBase,(void*)&Player.baseadd,4); // Get our players Base Address from the pointer
/*****made by stickleback******/
Player.coordEWa = Player.baseadd + 0ÃƒÆ’Ã¢â‚¬â€8; // Get all the addies for everythingÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦the 0ÃƒÆ’Ã¢â‚¬â€8, 0xC and **** are the offsets I found for DFX
Player.coordNSa = Player.baseadd + 0xC;
Player.coordUDa = Player.baseadd + 0ÃƒÆ’Ã¢â‚¬â€10;
Player.lookXa = Player.baseadd + 0ÃƒÆ’Ã¢â‚¬â€14;
Player.lookYa = Player.baseadd + 0ÃƒÆ’Ã¢â‚¬â€18;
Player.namea = Player.baseadd + 0xF4;
Peek((void*)Player.coordEWa,(void*)&Player.coordEW ,4); // Now we got all the addies, read in the info from em all
Peek((void*)Player.coordNSa,(void*)&Player.coordNS ,4);
Peek((void*)Player.coordUDa,(void*)&Player.coordUD ,4);
Peek((void*)Player.lookXa,(void*)&Player.lookX,4);
Peek((void*)Player.lookYa,(void*)&Player.lookY,4);
Peek((void*)Player.namea,(void*)&Player.name,15);

return Player; // Give our PLAYER_DATA Player, as the return value
}
///
PLAYER_DATA GetPlayerData(BYTE PlayerNum) // Takes the number of the player as a param
{
PLAYER_DATA Player;
ZeroMemory(&Player, sizeof(PLAYER_DATA));
Peek((void*)hBase,(void*)&Player.baseadd,4);

Player.baseadd = Player.baseadd + (PlayerNum*0ÃƒÆ’Ã¢â‚¬â€388); // 0ÃƒÆ’Ã¢â‚¬â€388 is the gap between players, starting with player 1

Player.coordEWa = Player.baseadd + 0ÃƒÆ’Ã¢â‚¬â€8; 
Player.coordNSa = Player.baseadd + 0xC;
Player.coordUDa = Player.baseadd + 0ÃƒÆ’Ã¢â‚¬â€10;
Player.lookXa = Player.baseadd + 0ÃƒÆ’Ã¢â‚¬â€14;
Player.lookYa = Player.baseadd + 0ÃƒÆ’Ã¢â‚¬â€18;
Player.namea = Player.baseadd + 0xF4;

Peek((void*)Player.coordEWa,(void*)&Player.coordEW ,4); 
Peek((void*)Player.coordNSa,(void*)&Player.coordNS ,4);
Peek((void*)Player.coordUDa,(void*)&Player.coordUD ,4);
Peek((void*)Player.lookXa,(void*)&Player.lookX,4);
Peek((void*)Player.lookYa,(void*)&Player.lookY,4);
Peek((void*)Player.namea,(void*)&Player.name,15);

return Player;
}
///
void SetCrosshairOnEnemy(BYTE PlayerNumber)
{
PLAYER_DATA oP = GetPlayerData(PlayerNumber); // oP = OppositionÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢s Player
PLAYER_DATA cP = GetMyPlayerData(); // cP = Current Player (our player) .. sorry for bad var names 

/*Sec 1*/
if(oP.coordEW > cP.coordEW && oP.coordNS <= cP.coordNS)
{
}

/*Sec 2*/
if(oP.coordEW <= cP.coordEW && oP.coordNS < cP.coordNS)
{
}

/*Sec 3*/
if(oP.coordEW < cP.coordEW && oP.coordNS >= cP.coordNS)
{
}

/*Sec 4*/
if(oP.coordEW >= cP.coordEW && oP.coordNS > cP.coordNS)
{
}
} 
void SetCrosshairOnEnemy(BYTE PlayerNumber)
{
PLAYER_DATA oP = GetPlayerData(PlayerNumber);
PLAYER_DATA cP = GetMyPlayerData(); 

double EWdif; // These need to be double for our Trig calculations to work later on 
double NSdif;

/*Sec 1*/
if(oP.coordEW > cP.coordEW && oP.coordNS <= cP.coordNS)
{
EWdif = oP.coordEW - cP.coordEW;
NSdif = cP.coordNS - oP.coordNS;
}

/*Sec 2*/
if(oP.coordEW <= cP.coordEW && oP.coordNS < cP.coordNS)
{
EWdif = cP.coordEW - oP.coordEW;
NSdif = cP.coordNS - oP.coordNS;
}

/*Sec 3*/
if(oP.coordEW < cP.coordEW && oP.coordNS >= cP.coordNS)
{
EWdif = cP.coordEW - oP.coordEW;
NSdif = oP.coordNS - cP.coordNS;
}

/*Sec 4*/
if(oP.coordEW >= cP.coordEW && oP.coordNS > cP.coordNS)
{
EWdif = oP.coordEW - cP.coordEW;
NSdif = oP.coordNS - cP.coordNS;
}
}
void SetCrosshairOnEnemy(BYTE PlayerNumber)
{
PLAYER_DATA oP = GetPlayerData(PlayerNumber);
PLAYER_DATA cP = GetMyPlayerData(); 

double EWdif;
double NSdif;
double angleA; // The angle in degrees between the enemy, east, and us
double angleP; // The decimal percentage of the angle

/*Sec 1*/
if(oP.coordEW > cP.coordEW && oP.coordNS <= cP.coordNS)
{
EWdif = oP.coordEW - cP.coordEW;
NSdif = cP.coordNS - oP.coordNS;
angleA = atan(NSdif/EWdif) * 57.29578; // Remember, the 57.29578 is to convert from radians to degrees 
angleP = (angleA/360);
}

/*Sec 2*/
if(oP.coordEW <= cP.coordEW && oP.coordNS < cP.coordNS)
{
EWdif = cP.coordEW - oP.coordEW;
NSdif = cP.coordNS - oP.coordNS;
angleA = atan(NSdif/EWdif) * 57.29578;
angleP = (angleA/360);
}

/*Sec 3*/
if(oP.coordEW < cP.coordEW && oP.coordNS >= cP.coordNS)
{
EWdif = cP.coordEW - oP.coordEW;
NSdif = oP.coordNS - cP.coordNS;
angleA = atan(NSdif/EWdif) * 57.29578;
angleP = (angleA/360);
}

/*Sec 4*/
if(oP.coordEW >= cP.coordEW && oP.coordNS > cP.coordNS)
{
EWdif = oP.coordEW - cP.coordEW;
NSdif = oP.coordNS - cP.coordNS;
angleA = atan(NSdif/EWdif) * 57.29578;
angleP = (angleA/360);
}
}
void SetCrosshairOnEnemy(BYTE PlayerNumber)
{
PLAYER_DATA oP = GetPlayerData(PlayerNumber);
PLAYER_DATA cP = GetMyPlayerData(); 

double EWdif;
double NSdif;
double angleA;
double angleP;
double newValue; // To hold our new double value
DWORD newValue2; // To convert our double back into DWORD ready for writing

double halfCircle = 0xFFFFFFFF/2; // Just to make the code a bit more readable 

/*Sec 1*/
if(oP.coordEW > cP.coordEW && oP.coordNS <= cP.coordNS)
{
EWdif = oP.coordEW - cP.coordEW;
NSdif = cP.coordNS - oP.coordNS;
angleA = atan(NSdif/EWdif) * 57.29578;
angleP = (angleA/360);
newValue = 0xFFFFFFFF - (0xFFFFFFFF*angleP); // As described above 
newValue2 = newValue; // Put it into DWORD (may get compile warnings about losing data..thats the whole reason weÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢re doing it 
Poke((void*)cP.lookXa, &newValue2,4); // Write our new value
}

/*Sec 2*/
if(oP.coordEW <= cP.coordEW && oP.coordNS < cP.coordNS)
{
EWdif = cP.coordEW - oP.coordEW;
NSdif = cP.coordNS - oP.coordNS;
angleA = atan(NSdif/EWdif) * 57.29578;
angleP = (angleA/360);
newValue = halfCircle + (0xFFFFFFFF*angleP);
newValue2 = newValue;
Poke((void*)cP.lookXa, &newValue2,4);
}

/*Sec 3*/
if(oP.coordEW < cP.coordEW && oP.coordNS >= cP.coordNS)
{
EWdif = cP.coordEW - oP.coordEW;
NSdif = oP.coordNS - cP.coordNS;
angleA = atan(NSdif/EWdif) * 57.29578;
angleP = (angleA/360);
newValue = halfCircle - (0xFFFFFFFF*angleP);
newValue2 = newValue;
Poke((void*)cP.lookXa, &newValue2,4);
}

/*Sec 4*/
if(oP.coordEW >= cP.coordEW && oP.coordNS > cP.coordNS)
{
EWdif = oP.coordEW - cP.coordEW;
NSdif = oP.coordNS - cP.coordNS;
angleA = atan(NSdif/EWdif) * 57.29578;
angleP = (angleA/360);
newValue = 0 + (0xFFFFFFFF*angleP);
newValue2 = newValue;
Poke((void*)cP.lookXa, &newValue2,4);
}
}
void SetCrosshairOnEnemy(BYTE PlayerNumber)
{
PLAYER_DATA oP = GetPlayerData(PlayerNumber);
PLAYER_DATA cP = GetMyPlayerData(); 

double EWdif;
double NSdif;
double UDdif;

double angleA;
double angleP;
double angleB;
double angleBP;

double newValue;
DWORD newValue2;

double newValueb;
DWORD newValueb2;

double halfCircle = 0xFFFFFFFF/2;

/*Sec 1*/
if(oP.coordEW > cP.coordEW && oP.coordNS <= cP.coordNS)
{
EWdif = oP.coordEW - cP.coordEW;
NSdif = cP.coordNS - oP.coordNS;
angleA = atan(NSdif/EWdif) * 57.29578;
angleP = (angleA/360);
newValue = 0xFFFFFFFF - (0xFFFFFFFF*angleP);
newValue2 = newValue;
Poke((void*)cP.lookXa, &newValue2,4);
}

/*Sec 2*/
if(oP.coordEW <= cP.coordEW && oP.coordNS < cP.coordNS)
{
EWdif = cP.coordEW - oP.coordEW;
NSdif = cP.coordNS - oP.coordNS;
angleA = atan(NSdif/EWdif) * 57.29578;
angleP = (angleA/360);
newValue = halfCircle + (0xFFFFFFFF*angleP);
newValue2 = newValue;
Poke((void*)cP.lookXa, &newValue2,4);
}

/*Sec 3*/
if(oP.coordEW < cP.coordEW && oP.coordNS >= cP.coordNS)
{
EWdif = cP.coordEW - oP.coordEW;
NSdif = oP.coordNS - cP.coordNS;
angleA = atan(NSdif/EWdif) * 57.29578;
angleP = (angleA/360);
newValue = halfCircle - (0xFFFFFFFF*angleP);
newValue2 = newValue;
Poke((void*)cP.lookXa, &newValue2,4);
}

/*Sec 4*/
if(oP.coordEW >= cP.coordEW && oP.coordNS > cP.coordNS)
{
EWdif = oP.coordEW - cP.coordEW;
NSdif = oP.coordNS - cP.coordNS;
angleA = atan(NSdif/EWdif) * 57.29578;
angleP = (angleA/360);
newValue = 0 + (0xFFFFFFFF*angleP);
newValue2 = newValue;
Poke((void*)cP.lookXa, &newValue2,4);
}

// Done the X-look, now this is for the Y-look

double flatDist = sqrt((EWdif*EWdif)+(NSdif*NSdif)); // Get the level distance between us and the enemy, using pythagoras

if(oP.coordUD == cP.coordUD)
{
BYTE zero4[4] = {0ÃƒÆ’Ã¢â‚¬â€00,0ÃƒÆ’Ã¢â‚¬â€00,0ÃƒÆ’Ã¢â‚¬â€00,0 ÃƒÆ’Ã¢â‚¬â€00};
Poke((void*)cP.lookYa,zero4, 4); // If we are equal height, set our Y-look to 0 (level)

} else if(oP.coordUD > cP.coordUD)
{
UDdif = oP.coordUD - cP.coordUD; // Work out our UDdif
angleB = atan(UDdif/flatDist) * 57.29578; // Same old stuff as before
angleBP = (angleB/360);
newValueb = 0 + (0xFFFFFFFF*angleBP);
newValueb2 = newValueb;
Poke((void*)cP.lookYa, &newValueb2,4);

} else if (oP.coordUD < cP.coordUD)
{
UDdif = cP.coordUD - oP.coordUD;
angleB = atan(UDdif/flatDist) * 57.29578;
angleBP = (angleB/360);
newValueb = 0xFFFFFFFF - (0xFFFFFFFF*angleBP);
newValueb2 = newValueb;
Poke((void*)cP.lookYa, &newValueb2,4);
}
}
