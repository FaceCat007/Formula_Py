CONST SHORT=12;CONST LONG=26;CONST MID=9;

DIF:EMA(VOL,SHORT)-EMA(VOL,LONG);
DEA:EMA(DIF,MID);
MACD:DIF-DEA,COLORSTICK;