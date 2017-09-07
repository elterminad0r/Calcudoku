# Calcudoku
A simple brute force solver for an 8\*8 'calcudoku'. A `Calcudoku` is given a number of *regions*, with *targets* and *operations*. A region is a set of adjacent cells (although the program could handle non-adjacent cells), where they are given an operation and a target. The Target is an integer which must be reached by combining the integers in the cells using the operation, ie:

    target = 6

operation | explanation
--- | ---
\+ | The numbers should add up to 6.
\- | The largest number subtract *all* the rest of the numbers should be 6.
\* | The product of the numbers should be 6.
/ | The largest number divided by *all* the rest of the numbers should be 6.

These regions are modelled in a pretty nicely structured OO model.

Input works like so: each region is defined and assigned to a character, and then a grid of characters is provided. You can refer to [ex.txt](https://github.com/elterminad0r/Calcudoku/blob/master/ex.txt) for a fully specified input file. Using it as input, with `cat ex.txt | python interf.py`, this output is produced:

    8 5 7 1 4 2 3 6 
    7 3 4 5 6 1 2 8 
    4 7 2 3 8 6 1 5 
    3 1 8 6 2 4 5 7 
    5 8 6 2 7 3 4 1 
    6 2 1 4 5 8 7 3 
    2 6 3 7 1 5 8 4 
    1 4 5 8 3 7 6 2 
