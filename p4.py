from random import choice, randint
from string import ascii_lowercase as al
import sys

# take user input and ensure in ranges
try:
	p = int(input("ptrn lngth: "))
	u = int(input("uniq chars: "))
	s = int(input("slot lngth: "))
except:
	sys.exit("input numbers")

if p not in range(10,101): sys.exit("out of range")
if u not in range(2,11):   sys.exit("out of range")
if s not in range(2,11):   sys.exit("out of range")

# generate list of possible letter choices
choices = list(al)[:u]
# generate pattern
pattern = [choice(choices) for f in range(p)]
# ensure all choices occur at least once
for f in choices:
	if f not in pattern: pattern[randint(0,len(pattern))] = f

# initialize slots
slots = [None for f in range(s)]

def FIFO(p,s):
	# slot index to replace
	i = 0

	# return struct
	t = [FIFO.__name__ + "  " + str(f) + ": " for f in range(len(s) + 1)]
	t[0] = "Ref Str: " + "".join(p)

	# for each item in pattern
	for f in p:
		# if item exists in slots, write cache hit
		if f in s:

			for g in range(1,len(t)):
				if g - 1 == s.index(f): t[g] += "*"
				else: t[g] += " "

		# if empty slot exists
		elif None in s:

			# write cache miss
			for g in range(1,len(t)):
				if g - 1 == s.index(None): t[g] += f
				else: t[g] += " "

			# set first empty slot to item
			s[s.index(None)] = f

		# if no empty slots exist
		else:

			# write cache miss
			for g in range(1,len(t)):
				if g - 1 == i: t[g] += f
				else: t[g] += " "

			# replace slot at index
			s[i] = f
			# if index to replace is small, increment
			if i < len(s) - 1:
				i += 1
			# otherwise, wrap to 0
			else:
				i = 0

	return(t)

def pr(s):
	for f in s:
		print(f)

pr(FIFO(pattern,slots))
