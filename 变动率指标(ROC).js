CONST N=12;CONST M=6;

ROC:100*(CLOSE-REF(CLOSE,N))/REF(CLOSE,N);
MAROC:MA(ROC,M);