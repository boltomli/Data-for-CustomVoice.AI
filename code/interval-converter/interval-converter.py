import argparse
import re
from os import mkdir
from os.path import exists, join

import tgt

parser = argparse.ArgumentParser(description='Convert interval')
parser.add_argument('intervalFile', metavar='IntervalFile', type=str,
                    help='Interval TextGrid file in ooTextFile format.')
parser.add_argument('segmentFolder', metavar='SegmentFolder', type=str,
                    help='Segment folder to save result.')
args = parser.parse_args()

text_grid = tgt.io.read_textgrid(args.intervalFile)
assert len(text_grid.tiers) == 1

intervals = text_grid.tiers[0].intervals
assert len(intervals) > 2
assert intervals[0].text == 'sil'
assert intervals[-1].text == 'sil'

name = text_grid.tiers[0].name.split('.')[0]

segments = []
a = iter(list(range(len(intervals))))

for i in a:
    # sp is treated as sil
    if 'sil' in intervals[i].text or 'sp' in intervals[i].text:
        segments.append('{start_time}\t{text}'.format(start_time=intervals[i].start_time, text='sil'))
    # Syllable with ending
    elif re.compile(r'\d').search(intervals[i].text):
        segments.append('{start_time}\t{text}'.format(start_time=intervals[i].start_time, text=intervals[i].text))
    # Syllable without ending
    else:
        syllable = ''.join([intervals[i].text, intervals[i+1].text])
        segments.append('{start_time}\t{text}'.format(start_time=intervals[i].start_time, text=syllable))
        next(a)

if not exists(args.segmentFolder):
    mkdir(args.segmentFolder)
with(open(join(args.segmentFolder, name + '.txt'), 'w', encoding='utf-8')) as f:
    f.write('\r\n'.join(segments))
