CONST N=10;

VAR1:=MA((VOL-REF(VOL,1))/REF(VOL,1),5);
VAR2:=(CLOSE-MA(CLOSE,24))/MA(CLOSE,24)*100;
MY: VAR2*(1+VAR1);
SHT: MY, COLORSTICK;
SHTMA: MA(SHT,N);