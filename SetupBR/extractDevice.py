#!/usr/bin/env python

import sys
import re

a = sys.argv[1]
e = re.findall(r'[\w\.-]+', a)

for i in e:
    if i == '0':
        print e[1]
        sys.exit(0)
