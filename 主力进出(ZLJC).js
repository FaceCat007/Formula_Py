﻿VAR1:=(CLOSE+LOW+HIGH)/3; 
VAR2:=SUM(((VAR1-REF(LOW,1))-(HIGH-VAR1))*VOL/100000/(HIGH-LOW),0); 
VAR3:=EMA(VAR2,1); 
JCS:VAR3; 
JCM:MA(VAR3,12); 
JCL:MA(VAR3,26);