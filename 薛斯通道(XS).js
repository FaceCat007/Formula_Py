﻿CONST N=13;

VAR2:=CLOSE*VOL;
VAR3:=EMA((EMA(VAR2,3)/EMA(VOL,3)+EMA(VAR2,6)/EMA(VOL,6)+EMA(VAR2,12)/EMA(VOL,12)+EMA(VAR2,24)/EMA(VOL,24))/4,N);
SUP:1.06*VAR3;
SDN:VAR3*0.94;
VAR4:=EMA(CLOSE,9);
LUP:EMA(VAR4*1.14,5);
LDN:EMA(VAR4*0.86,5);