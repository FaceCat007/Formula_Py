VAR1:=CLOSE-LOW;
VAR2:=HIGH-LOW;
VAR3:=CLOSE-HIGH;
VAR4:=IF(CLOSE>=0,(VAR1/VAR2+VAR3/VAR2)*VOL,(VAR3/VAR2+VAR1/VAR2)*VOL);
CYW: SUM(VAR4,10)/10000, COLORSTICK;