class mode:

	'''The mode class'''

	def __init__(self, normalisation, instancename):
		self.norm = normalisation
		self.name = instancename

	def __repr__(self):
		
		return self.name


	def what(self):

		print self.norm
		print self.name


mode1 = mode(2,"Jim")

#mode1.what()

print "The normalisation is: ", mode1.norm
print "The mode name is: ", mode1
