# Ranked Choice Voting tabulator
### To verify 2018 Maine CD2 Ranked Choice Voting election results
### Scotty Vercoe, November 2018

**This code was written to verify the official results of the first Ranked Choice Voting election in the history of the United States.**

The election turned out to be remarkably transparent. Since the incumbent has charged that RCV is a "black box" I thought it important to dispel any false notions, and show how cleanly and simply the system works.

### Get the data
Download all the CSV files I provide (there are 8)

**OR**
1. Download all "DISTRICT 2 FINAL" files from the Secretary of State's Office.
2. Convert them all to CSV, putting them all in the same folder.

### Run the script
Download rcv.py, and place in the same folder as the CSV files.
At a command prompt/terminal, type
```
python rcv.py
```
Ballots are loaded, then the tabulator runs the instant runoffs:
```
296077 ballots collected!
207487 ballots adjusted for undervotes
1453 ballots adjusted for invalidated/overvotes
=============== ROUND 1 ===============
Bond, Tiffany L.       16552    5.71%
DEM Golden, Jared F.  132013   45.58%
Hoar, William R.S.      6875    2.37%
REP Poliquin, Bruce   134184   46.33%
=== NO WINNER YET! (6453 exhausted) ===
...dropping loser: Hoar, William R.S.

=============== ROUND 2 ===============
Bond, Tiffany L.       19173    6.67%
DEM Golden, Jared F.  133216   46.34%
Hoar, William R.S.         0    0.00%
REP Poliquin, Bruce   135073   46.99%
=== NO WINNER YET! (8615 exhausted) ===
...dropping loser: Bond, Tiffany L.

=============== ROUND 3 ===============
Bond, Tiffany L.           0    0.00%
DEM Golden, Jared F.  142440   50.62%
Hoar, William R.S.         0    0.00%
REP Poliquin, Bruce   138931   49.38%

WINNER is DEM Golden, Jared F. with 50.62% of the vote!
(14706 ballots exhausted)
```

### Running on other elections
The tabulator can be used to run any Ranked Choice Voting election with any size list of ballots, where each ballot itself is a ranked list.

While the ballots list contain indexed candidates (by int), the program uses a single key of candidates for human-readable output. The same key is used to read the ballots from CSV files.

Make your ranked choice ballots a list of lists of ints:
```
[ [0,4,1], [2,3,0], ... ]
```
#### Ballots can be different lengths w/ incomplete rankings
If you have other ballots as CSV files, just change fields to specify which fields in the CSV contain rankings. Make your key of indexed candidates.
#### Key needs to be as long as your longest ballot
Currently, two fields overvote/undervote are in the key. Remove these fields from the key, and change the init value for dropped to an empty list.

Edit or remove the ballot rules as needed.
