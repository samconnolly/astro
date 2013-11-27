def eat(x):
	y = x + 3
	return y

def sleep(x):
	y = x - 3
	return y

def choose(x,func):
	y = func(x)
	return y

print choose(4,eat)
print choose(4,sleep)

