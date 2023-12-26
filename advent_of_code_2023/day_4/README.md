
How to get the number of instances for each card:
1. For each card, count the number of matching numbers as describe in part 1. 
   This number now represent the number of cards below the current one that must be copied.
2. For each copied card to copy, increment the 'instances' counter by current card's 'instances' counter. 

Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53     4 matches
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19     2 matches
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1     2 match
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83     1 match
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36     0 match
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11     0 match

---- Running the algorithm ----
{instances: 1} Card 1 has 4 matches => copy of cards: 2, 3, 4, 5
{instances: 2} Card 2 has 2 matches => copy of cards: 3, 4
{instances: 4} Card 3 has 2 matches => copy of cards: 4, 5
{instances: 8} Card 4 has 1 match => copy of cards: 5
{instances: 14} Card 5 has 0 matches => copy of cards: none
{instances: 1} Card 6 has 0 matches => copy of cards: none


