VAR1:=REF(MA(CLOSE,20),10); 
开:=OPEN-VAR1; 
高:=HIGH-VAR1; 
低:=LOW-VAR1; 
收:=CLOSE-VAR1; 
MID:=MA(CLOSE,20);
UPPER:=MID+2*STD(CLOSE,20);
LOWER:=MID-2*STD(CLOSE,20); 
V1:=(CLOSE-LOWER)/(UPPER-LOWER)*100; 
V2:=V1-EMA(V1,5);
K1:=SUM(LLV(V2,4),4)/4;
V3:=EMA(V2,64)*10; 
V4:=EMA(0.4*V2*(-1),3); 
V5:=-1*EMA(V2,39)*10; 
A:=V3>10; 
B:=V2>V4; 
D:=V5>10; 
E:=V3<=10 OR V2<=V4 OR V5<=10; 
STICKLINE(收>=开 AND E,CLOSE,OPEN,2.5,0) ,COLORYELLOW; 
STICKLINE(收<开 AND E,CLOSE,OPEN,2.5,0),COLORYELLOW;
STICKLINE(开>收 AND A,CLOSE,OPEN,2.5,0),COLORFF0000; 
STICKLINE(开<=收 AND A,CLOSE,OPEN,2.5,0),COLORYELLOW; 
STICKLINE(开>收 AND B,CLOSE,OPEN,2.5,0),COLORFF00FF; 
STICKLINE(开<=收 AND B,CLOSE,OPEN,2.5,0),COLORFF00FF; 
STICKLINE(开>收 AND D,CLOSE,OPEN,2.5,0),COLORGREEN;