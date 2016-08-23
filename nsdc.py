#!/usr/bin/env python
from noxscript import decompiler
import sys

decompiler.Decompiler(open(sys.argv[1], 'rb'))
