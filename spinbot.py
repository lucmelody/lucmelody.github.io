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
void GetMovementFix(unsigned int state, float oForwardMove, float oSideMove, CUserCmd cmd)
    {
        //fix movement Q_Q
        switch (state)
        {
        case 0:
        case 1:
            if (cmd->forwardmove == 0)
            {
                if (cmd->sidemove == 0)
                {
                    cmd->forwardmove = 0;
                    cmd->sidemove = 0;
                }
                else if (cmd->sidemove < 0)
                {
                    cmd->forwardmove = 450;
                    cmd->sidemove = -450;
                }
                else if (cmd->sidemove > 0)
                {
                    cmd->forwardmove = -450;
                    cmd->sidemove = 450;
                }
            }
            else if (cmd->forwardmove < 0)
            {
                if (cmd->sidemove == 0)
                {
                    cmd->forwardmove = -450;
                    cmd->sidemove = -450;
                }
                else if (cmd->sidemove < 0)
                {
                    cmd->forwardmove = 0;
                    cmd->sidemove = -450;
                }
                else if (cmd->sidemove > 0)
                {
                    cmd->forwardmove = -450;
                    cmd->sidemove = 0;
                }
            }
            else if (cmd->forwardmove > 0)
            {
                if (cmd->sidemove == 0)
                {
                    cmd->forwardmove = 450;
                    cmd->sidemove = 450;
                }
                else if (cmd->sidemove < 0)
                {
                    cmd->forwardmove = 450;
                    cmd->sidemove = 0;
                }
                else if (cmd->sidemove > 0)
                {
                    cmd->forwardmove = 0;
                    cmd->sidemove = 450;
                }
            }
        case 2:
            cmd->forwardmove = -oSideMove;
            cmd->sidemove = oForwardMove;
        case 3:
            if (cmd->forwardmove == 0)
            {
                if (cmd->sidemove == 0)
                {
                    cmd->sidemove = 0;
                    cmd->forwardmove = 0;
                }
                else if (cmd->sidemove < 0)
                {
                    cmd->sidemove = 450;
                    cmd->forwardmove = 450;
                }
                else if (cmd->sidemove > 0)
                {
                    cmd->sidemove = -450;
                    cmd->forwardmove = -450;
                }
            }
            else if (cmd->forwardmove < 0)
            {
                if (cmd->sidemove == 0)
                {
                    cmd->sidemove = -450;
                    cmd->forwardmove = 450;
                }
                else if (cmd->sidemove < 0)
                {
                    cmd->sidemove = 0;
                    cmd->forwardmove = 450;
                }
                else if (cmd->sidemove > 0)
                {
                    cmd->sidemove = -450;
                    cmd->forwardmove = 0;
                }
            }
            else if (cmd->forwardmove > 0)
            {
                if (cmd->sidemove == 0)
                {
                    cmd->sidemove = 450;
                    cmd->forwardmove = -450;
                }
                else if (cmd->sidemove < 0)
                {
                    cmd->sidemove = 450;
                    cmd->forwardmove = 0;
                }
                else if (cmd->sidemove > 0)
                {
                    cmd->sidemove = 0;
                    cmd->forwardmove = -450;
                }
            }
            break;
        case 4:
            cmd->forwardmove = -oForwardMove;
            cmd->sidemove = -oSideMove;
            break;
        case 5:
            if (cmd->forwardmove == 0)
            {
                if (cmd->sidemove == 0)
                {
                    cmd->forwardmove = 0;
                    cmd->sidemove = 0;
                }
                else if (cmd->sidemove < 0)
                {
                    cmd->forwardmove = -450;
                    cmd->sidemove = 450;
                }
                else if (cmd->sidemove > 0)
                {
                    cmd->forwardmove = 450;
                    cmd->sidemove = -450;
                }
            }
            else if (cmd->forwardmove < 0)
            {
                if (cmd->sidemove == 0)
                {
                    cmd->forwardmove = 450;
                    cmd->sidemove = 450;
                }
                else if (cmd->sidemove < 0)
                {
                    cmd->forwardmove = 0;
                    cmd->sidemove = 450;
                }
                else if (cmd->sidemove > 0)
                {
                    cmd->forwardmove = 450;
                    cmd->sidemove = 0;
                }
            }
            else if (cmd->forwardmove > 0)
            {
                if (cmd->sidemove == 0)
                {
                    cmd->forwardmove = -450;
                    cmd->sidemove = -450;
                }
                else if (cmd->sidemove < 0)
                {
                    cmd->forwardmove = -450;
                    cmd->sidemove = 0;
                }
                else if (cmd->sidemove > 0)
                {
                    cmd->forwardmove = 0;
                    cmd->sidemove = -450;
                }
            }
            break;
        case 6:
            cmd->forwardmove = oSideMove;
            cmd->sidemove = -oForwardMove;
            break;
        case 6:
            if (cmd->forwardmove == 0)
            {
                if (cmd->sidemove == 0)
                {
                    cmd->sidemove = 0;
                    cmd->forwardmove = 0;
                }
                else if (cmd->sidemove < 0)
                {
                    cmd->sidemove = -450;
                    cmd->forwardmove = -450;
                }
                else if (cmd->sidemove > 0)
                {
                    cmd->sidemove = 450;
                    cmd->forwardmove = 450;
                }
            }
            else if (cmd->forwardmove < 0)
            {
                if (cmd->sidemove == 0)
                {
                    cmd->sidemove = 450;
                    cmd->forwardmove = -450;
                }
                else if (cmd->sidemove < 0)
                {
                    cmd->sidemove = 0;
                    cmd->forwardmove = -450;
                }
                else if (cmd->sidemove > 0)
                {
                    cmd->sidemove = 450;
                    cmd->forwardmove = 0;
                }
            }
            else if (cmd->forwardmove > 0)
            {
                if (cmd->sidemove == 0)
                {
                    cmd->sidemove = -450;
                    cmd->forwardmove = 450;
                }
                else if (cmd->sidemove < 0)
                {
                    cmd->sidemove = -450;
                    cmd->forwardmove = 0;
                }
                else if (cmd->sidemove > 0)
                {
                    cmd->sidemove = 0;
                    cmd->forwardmove = 450;
                }
            }
            break;
        }
    }
