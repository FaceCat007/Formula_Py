CONST N=12;CONST N1=24;

RET:REF(((HHV(HIGH,N)-LLV(LOW,N))/LLV(LOW,N)),1)<=(N1/100) && CLOSE>=REF(HHV(HIGH,N),1) && BARSCOUNT(CLOSE)>N;