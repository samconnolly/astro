class animal:
	def __init__(self,name, num):
		self.num  = num
		self.name = name

	def __str__(self):
		return self.name

	def numref(self):
		print "the dog is called {0} and has {0.num}".format(self)

Jim = animal("Jim",1)
Jim.numref()
