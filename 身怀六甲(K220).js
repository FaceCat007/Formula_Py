KSTAR:ABS(REF(CLOSE,1)-REF(OPEN,1))/REF(CLOSE,1)>0.04&&
ABS(CLOSE-OPEN)/CLOSE<0.005&&
MAX(CLOSE,OPEN)<MAX(REF(CLOSE,1),REF(OPEN,1))&&
MIN(CLOSE,OPEN)>MIN(REF(CLOSE,1),REF(OPEN,1));