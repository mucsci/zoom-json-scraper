#!/usr/bin/env python3

import json
import sys
from collections import defaultdict
from statistics import pstdev, mean

def read_file(name):
    with open(name) as f:
        return json.load(f)

def calc_durations(data, **kwargs):
    prof, start, end = kwargs['prof'], kwargs['start'], kwargs['end']
    durations = defaultdict(int)
    for entry in data['attendees']:
        if entry['email'] == prof:
            continue
        if entry['join'] < start:
            entry['duration'] -= (start - entry['join'])
            entry['join'] = start
        if entry['join'] + entry['duration'] > end:
            entry['duration'] = end - entry['join']
        if (entry['duration'] < 0):
            entry['duration'] = 0
        durations[entry['name']] += entry['duration']
    return durations

def make_report(durations):
    xbar = mean(t for _,t in durations.items())
    s = pstdev((t for _,t in durations.items()), xbar)
    for e, x in durations.items():
        z = (x - xbar) / s
        status = 'L' if (x - xbar) / s < -1.0 else 'P'
        yield (status,e,z)

def main(prof, filename, offset=None, duration=None):
    data = read_file(filename)
    start = min(e['join'] for e in data['attendees'] if e['email'] == prof)
    end = max(e['join'] + e['duration'] for e in data['attendees'] if e['email'] == prof)
    if offset:
        start += 60*int(offset)
    if duration:
        end = start + 60 * int(duration)
    durations = calc_durations(data, prof=prof, start=start, end=end)
    zscores = sorted(x for x in make_report(durations))
    for status,uid,score in zscores:
        print(f"{status} {uid:30} [{durations[uid]/60:3.0f} min] ({score:5.2f})")

if __name__ == '__main__':
    main(*sys.argv[1:])
