V1:=(CLOSE-LLV(LOW,36))/(HHV(HIGH,36)-LLV(LOW,36))*100; 
V2:=SMA(V1,4,1); 
V3:=SMA(V2,4,1); 
V4:=SMA(V3,4,1); 
顶线:100; D:V4; 
底线:0; 
K:V3; 
低吸线:10,COLORGREEN,LINETHICK2;
高抛线:90,COLORRED,LINETHICK2; 
DRAWTEXT(CURRBARSCOUNT()=5,3,'潜伏'),COLORRED;
V6:=CROSS(V3,V4) AND V3<20; 
STICKLINE(K>D , K,D ,2.5,0),COLORRED,LINETHICK2; 
STICKLINE(D>K,K,D,2.5,0),COLORGREEN,LINETHICK2; 
V7:=CROSS(V4,V3) AND V3>80; 
V8:=CROSS(V2,V3) AND V3>80 AND V3>V4; 
DRAWTEXT(CROSS(K,11),5,'低买'); 
DRAWTEXT(CROSS(K,92),96,'大风险'); 
DRAWTEXT(CROSS(K,79),85,'小风险');