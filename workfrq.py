#!/usr/bin/env python
import operator
import subprocess
import time

handle=file('annotation.txt')
#sep = ['/', '-', '(', ')', ',' ]
frq={}
for line in handle:
    line = line.split()
    for word in line:
        if word in frq:
            frq[word] += 1
        else:
            frq[word] = 1
sorted_frq = sorted(frq.iteritems(), key = operator.itemgetter(1), reverse=True)
for item in sorted_frq:
    print item
    time.sleep(10)
    subprocess.call(["grep",item[0], "annotation.txt"])
    

handle.close()

