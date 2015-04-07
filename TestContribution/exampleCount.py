import json
import os
import re

class info:
    notebook = ''
    examples = []
notebooks = os.listdir('.')
notebooks = sorted(notebooks)
print notebooks

total = 0

for i in range(len(notebooks)):
    ch_examples = 0
    if notebooks[i].endswith(".ipynb"):
        f = open(notebooks[i],'r')
        data = json.load(f)
        for dic in data["worksheets"][0]["cells"][0:]:
            if "level" in dic and dic["level"] == 2:
                ch_examples += 1
        total += ch_examples
        print i, " :  " , ch_examples
        
                

print "Total Examples : " , total
