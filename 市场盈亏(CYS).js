CYC13:=0.01*EXPMA(AMOUNT,13)/EXPMA(VOL,13);
CYS:(CLOSE-CYC13)/CYC13*100;