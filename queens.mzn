include "all_different.mzn";
int: k;
array[1..k] of var 1..k: queens;
constraint all_different(queens);
constraint all_different([queens[i]+i | i in 1..k]);
constraint all_different([queens[i]-i | i in 1..k]);
solve satisfy;
