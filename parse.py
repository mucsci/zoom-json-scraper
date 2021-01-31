#!/usr/bin/env python3

import json
import sys
from collections import defaultdict
from statistics import pstdev, mean

def read_file(name):
    with open(name) as f:
        return json.load(f)

prof = sys.argv[1]
data = read_file(sys.argv[2])

start = min(e['join'] for e in data['attendees'] if e['email'] == prof)

durations = defaultdict(int)
for entry in data['attendees']:
    if entry['email'] == prof:
        continue
    if (entry['join'] < start):
        entry['duration'] -= (start - entry['join'])
    durations[entry['name']] += entry['duration']

xbar = mean(t for _,t in durations.items())
s = pstdev((t for _,t in durations.items()), xbar)
zscores = list((e,(x - xbar) / s) for e,x in durations.items())
zscores.sort(key=lambda x: x[0])
for uid,score in zscores:
    print(f"{'L' if score < -1.0 else 'P'} {uid:30} [{durations[uid]/60:3.0f} min] ({score:5.2f})")
