CONST N=14;

TYP:=(HIGH+LOW+CLOSE)/3; 
V1:=SUM(IF(TYP>REF(TYP,1),TYP*VOL,0),N)/SUM(IF(TYP<REF(TYP,1),TYP*VOL,0),N); 
MFI:100-(100/(1+V1));