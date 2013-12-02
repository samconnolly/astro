import inspect



def go(a,b):
	c = a + b
	return c

x = go(3,6)

print x

def play(f):
	for arg in len(inspect.getargspec(go)[0]):
	d = go(f)
	return d

q =[3,6]

y = len(inspect.getargspec(go)[0])
print y
