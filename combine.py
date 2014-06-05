"""
Combine minute dumps into a single file
"""
import sys
import json
import os
import csv
from datetime import datetime

data_dir = sys.argv[1]
output_prefix = sys.argv[2]
files = os.listdir(data_dir)

results = {}
header = {}
for f in files:
    abspath = os.path.abspath(os.path.join(data_dir, f))
    try:
        dt = datetime.strptime(f, '%y%m%d_%H%M%S.json')
    except ValueError:
        print 'ignoring', f
        continue
    print dt.isoformat()
    fh = open(abspath, 'rb')
    data = json.loads(fh.read())
    fh.close()

    number_of_cities = len(data)
    if number_of_cities not in results:
        results[number_of_cities] = []
        header[number_of_cities] = [x['name'] for x in data]
    thelist = results[number_of_cities]
    thelist.append([dt.isoformat()] + [x['votes'] for x in data])

for number in header:
    fh = open('%s%s.csv' % (output_prefix, number), 'wb')
    writer = csv.writer(fh)
    writer.writerow(['date'] + header[number])
    for row in results[number]:
        writer.writerow(map(str, row))
