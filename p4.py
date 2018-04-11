from random import choice, randint
from string import ascii_uppercase as au
from subprocess import run, PIPE
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
choices = list(au)[:u]
# generate pattern
pattern = [choice(choices) for f in range(p)]
# ensure all choices occur at least once
"""for f in pattern:
	for g in choices:
		if g not in pattern: pattern[randint(0,len(pattern) - 1)] = f
"""

# initialize slots
slots = [None for f in range(s)]

def FIFO(p,slots):
	# slot index to replace
	i = 0

	# duplicate slots to ensure function purity
	s = slots[:]

	# printing struct
	r = ["FIFO  " + str(f) + ": " for f in range(len(s) + 1)]
	r[0] = "Ref Str: " + " ".join(p)

	# for each item in pattern
	for f in p:

		# if item exists in slots
		if f in s:
			# write cache hit
			for g in range(1,len(r)):
				if g - 1 == s.index(f): r[g] += "+ "
				else: r[g] += "  "

		# if empty slot exists
		elif None in s:
			# write cache miss
			for g in range(1,len(r)):
				if g - 1 == s.index(None): r[g] += f + " "
				else: r[g] += "  "
			# set first empty slot to item
			s[s.index(None)] = f

		# if no empty slots exist
		else:
			# write cache miss
			for g in range(1,len(r)):
				if g - 1 == i: r[g] += f + " "
				else: r[g] += "  "
			# replace slot at index
			s[i] = f
			# if index to replace is small, increment
			if i < len(s) - 1:
				i += 1
			# otherwise, wrap to 0
			else:
				i = 0

	# return struct
	return(r)

def LRU(p,slots):
	# stores time index of when last used (hit, replacement)
	l = [0 for f in slots]

	# duplicate slots to ensure function purity
	s = slots[:]

	# printing struct
	r = ["LRU   " + str(f) + ": " for f in range(len(s) + 1)]
	r[0] = "Ref Str: " + " ".join(p)

	# for each item in pattern by index
	for f in range(len(p)):

		# if item exists in slots
		if p[f] in s:
			# write cache hit
			for g in range(1,len(r)):
				if g - 1 == s.index(p[f]): r[g] += "+ "
				else: r[g] += "  "
			# record time index of hit
			l[s.index(p[f])] = f

		# if empty slot exists
		elif None in s:
			# set slot index to first None
			i = s.index(None)
			# write cache miss
			for g in range(1,len(r)):
				if g - 1 == i: r[g] += p[f] + " "
				else: r[g] += "  "
			# set slot to missed item
			s[i] = p[f]
			# record time index of replacement
			l[i] = f

		# if no empty slots exist
		else:
			# index to replace is the least recently used item
			i = l.index(min(l))
			# write cache miss
			for g in range(1,len(r)):
				if g - 1 == i: r[g] += p[f] + " "
				else: r[g] += "  "
			# set slot to missed item
			s[i] = p[f]
			# record time index of replacement
			l[i] = f

	# return struct
	return(r)

def MIN(p,slots):
	# duplicate slots to ensure function purity
	s = slots[:]

	# printing struct
	r = ["MIN   " + str(f) + ": " for f in range(len(s) + 1)]
	r[0] = "Ref Str: " + " ".join(p)

	for f in range(len(p)):

		# if item exists in slots
		if p[f] in s:
			# write cache hit
			for g in range(1,len(r)):
				if g - 1 == s.index(p[f]): r[g] += "+ "
				else: r[g] += "  "

		# if empty slot exists
		elif None in s:
			# set slot index to first None
			i = s.index(None)
			# write cache miss
			for g in range(1,len(r)):
				if g - 1 == i: r[g] += p[f] + " "
				else: r[g] += "  "
			# set slot to missed item
			s[i] = p[f]

		# if no empty slots exist
		else:
			# index of next use in pattern
			il = []
			# find the index for each item in slot
			for g in s:
				if g in p[f:]:
					il.append(p[f:].index(g) + f)
				else:
					il.append(101)
			# set index to index of furthest item
			if 101 in il:
				# if it doesn't occur, just set it to the first one not to occur
				i = il.index(101)
			else:
				i = s.index(p[max(il)])
			# write cache miss
			for g in range(1,len(r)):
				if g - 1 == i: r[g] += p[f] + " "
				else: r[g] += "  "
			# set slot to missed item
			s[i] = p[f]

	# return struct
	return(r)

def RAND(p,slots):
	# duplicate slots to ensure function purity
	s = slots[:]

	# printing struct
	r = ["RAND  " + str(f) + ": " for f in range(len(s) + 1)]
	r[0] = "Ref Str: " + " ".join(p)

	for f in p:

		# if item exists in slots
		if f in s:
			# write cache hit
			for g in range(1,len(r)):
				if g - 1 == s.index(f): r[g] += "+ "
				else: r[g] += "  "

		# if empty slot exists
		elif None in s:
			# set slot index to first None
			i = s.index(None)
			# write cache miss
			for g in range(1,len(r)):
				if g - 1 == i: r[g] += f + " "
				else: r[g] += "  "
			# set slot to missed item
			s[i] = f

		# if no empty slots exist
		else:
			# random index
			i = randint(0,len(s) - 1)
			# write cache miss
			for g in range(1,len(r)):
				if g - 1 == i: r[g] += f + " "
				else: r[g] += "  "
			# set random slot to missed item
			s[i] = f

	# return struct
	return(r)

def pr(s):
	# disgusting hack to print according to spec on Linux
	wb = run(["tput", "cols"], stdout=PIPE)
	ws = wb.stdout.decode("utf-8")
	w = int("".join(ws.split()))
	for f in range((len(s[0]) // w) + 1):
		if f == 0:
			for g in s:
				print(g[:w])
		else:
			print("######## wrapping", f)
			for g in s:
				print(g[:8],g[(w * f) + 8:(w * f) + w - 2])

print()
fifo = FIFO(pattern,slots)
pr(fifo)
print(''.join(['-'] * (len("         " + ' '.join(pattern)) - 1)))
lru = LRU(pattern,slots)
pr(lru)
print(''.join(['-'] * (len("         " + ' '.join(pattern)) - 1)))
m = MIN(pattern,slots)
pr(m)
print(''.join(['-'] * (len("         " + ' '.join(pattern)) - 1)))
rand = RAND(pattern,slots)
pr(rand)

scores_counter = [fifo,lru,m,rand]
count = [0] * 4
for f in scores_counter:
	for g in f: count[scores_counter.index(f)] += g.count("+")
	for g in count: g /= p

scores = [f / p for f in count]

print("\nCache Hit Rates:\n")
print("FIFO : " + str(count[0]) + " of " + str(p) + " = " + str(scores[0]))
print("LRU  : " + str(count[1]) + " of " + str(p) + " = " + str(scores[1]))
print("MIN  : " + str(count[2]) + " of " + str(p) + " = " + str(scores[2]))
print("FIFO : " + str(count[3]) + " of " + str(p) + " = " + str(scores[3]))
print("\nBest:  " + scores_counter[scores.index(max(scores))][1][:4])
print("Worst: " + scores_counter[scores.index(min(scores))][1][:4])
