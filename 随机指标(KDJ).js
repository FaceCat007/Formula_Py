CONST N=9;CONST M1=3;CONST M2=3;

RSV:=(CLOSE-LLV(LOW,N))/(HHV(HIGH,N)-LLV(LOW,N))*100; K:SMA(RSV,M1,1); 
D:SMA(K,M2,1);
J:3*K-2*D;