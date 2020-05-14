#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os, sys, random
print('test')
dirs = os.scandir("./")

for file in dirs:
	print(file.name, file.is_file())
	# print()

print(random.randint(0,0))