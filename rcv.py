# Ranked Choice Voting election tabulator
# Created to verify results of 2018 Maine CD2 Congressional election data:
#     https://www.maine.gov/sos/cec/elec/results/results18.html#Nov6
# Using rules:
#     https://www.maine.gov/sos/cec/elec/upcoming/pdf/250rcvnew.pdf
# by Scotty Vercoe, November 2018
# FREE TO USE WITH ATTRIBUTION

import os
import csv
from operator import itemgetter

KEY = [
    'Bond, Tiffany L.',
    'DEM Golden, Jared F.',
    'Hoar, William R.S.',
    'REP Poliquin, Bruce',
    'undervote',
    'overvote'
]

def collect(fields=(3, 8)):
    'collect CSV files into single list of ballots; get ranked choices from given fields'
    
    ballots = []
    files = [x for x in os.listdir('.') if x.endswith('.csv')]
    
    for f in files:
        print 'Opening %s' % f
        with open('%s' % f) as fil:
            at = 0
            reedr = csv.reader(fil, delimiter=',')
            for row in reedr:
                if at != 0:
                    ballot = []
                    for x in range(*fields):
                        ballot.append(row[x])
                    ballots.append(ballot)
                at += 1
    
    print '%i ballots collected!' % len(ballots)
    return ballots

def process(ballots, key=KEY):
    'process ballots according to SoS rules and given key'
    
    # clean extraneous text
    ballots = [[x.replace('(5931)','').replace('(5471)','').strip() for x in b] for b in ballots]
    
    # RULE: two consecutive undervotes invalidate remaining rankings
    seen = 0
    for b in range(len(ballots)):
        for i in range(len(ballots[b])):
            if ballots[b][i:i+2] == ['undervote','undervote']:
                ballots[b] = ballots[b][:i] # apply undervote rule
                seen += 1
                break
    print '%i ballots adjusted for undervotes' % seen
    
    # RULE: overvotes invalidate remaining rankings
    seen = 0
    for b in range(len(ballots)):
        for i in range(len(ballots[b])):
            if ballots[b][i] in ('overvote','invalidated'):
                ballots[b] = ballots[b][:i] # apply overvote rule
                seen += 1
                break
    print '%i ballots adjusted for invalidated/overvotes' % seen
    
    return [[key.index(x) for x in b] for b in ballots]

def tabulate(ballots, key=KEY, dropped=[4,5]):
    'compute Ranked Choice Voting election from ballots, indexed by key; omit dropped choices'
    
    runoff = 0
    winner = 0
    voters = float(len(ballots))
    ranks = len(key) - len(dropped)
    
    # until a winner is found...
    while winner < 0.5:
        print '%s ROUND %i %s' % (15*'=', runoff+1, 15*'=')
        
        # new round tally
        tired = 0
        tally = dict([(rank, 0) for rank in range(ranks)])
        for ballot in ballots:
            
            # get this voters' top available choice
            for choice in ballot:
                if not choice in dropped:
                    tally[choice] += 1
                    break # vote tallied! next...
            else:
                tired += 1 # exhausted ballot :(
        
        # compute results & check for majority winner
        voters = float(len(ballots) - tired)
        percent = [(cand, votes/voters) for cand,votes in tally.iteritems()]
        ranking = sorted(percent, key=itemgetter(1))
        winner = ranking[-1][1] # leading candidate percentage
        
        for k,v in tally.iteritems():
            print key[k].ljust(21), str(v).rjust(6), ('%.2f%%' % (percent[k][1]*100)).rjust(8)
        
        if winner < 0.5:
            loser = ranking[runoff][0]
            dropped.append(loser)
            print '=== NO WINNER YET! (%i exhausted) ===' % tired
            print '...dropping loser: %s\n' % key[loser]
        runoff += 1
    
    print '\nWINNER is %s with %.2f%% of the vote!' % (key[ranking[-1][0]], winner*100)
    print '(%i ballots exhausted)' % tired

if __name__ == '__main__':
    ballots = process(collect(), KEY)
    tabulate(ballots, KEY)
