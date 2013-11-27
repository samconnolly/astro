def goat(a, b = None, c = False):
	print a
	if b:
		print b
	if c:
		print "true"

goat(1)

goat(1,2)

goat(1,2,True)

print "truth test"

a = []

if a:
	print"no"

a = [1]

if a:
	print"yes"
