CONST M=10;

MID:=(3*CLOSE+LOW+OPEN+HIGH)/6;
DKX:(20*MID+19*REF(MID,1)+18*REF(MID,2)+17*REF(MID,3)+
16*REF(MID,4)+15*REF(MID,5)+14*REF(MID,6)+
13*REF(MID,7)+12*REF(MID,8)+11*REF(MID,9)+
10*REF(MID,10)+9*REF(MID,11)+8*REF(MID,12)+
7*REF(MID,13)+6*REF(MID,14)+5*REF(MID,15)+
4*REF(MID,16)+3*REF(MID,17)+2*REF(MID,18)+REF(MID,20))/210;
MADKX:MA(DKX,M);