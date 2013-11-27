# callgroupxspec.py - callable

# Uses the HEADAS tool grppha to group a given x-ray spectrum uninteractively
# Uses input spectrum to create output filenames and assign
# background and response files, using commands of the format:
# 'grppha spec.pha !out.pha comm = "chkey BACKFILE back.pha & chkey RESPFILE 
# file.rmf & chkey ANCRFILE file.arf & group min 15 & exit" '
 
# Sam Connolly 14/02/13

import os

# ==============================================================================

def group(spectrum,output,route,groupcommand,overwrite = True):


	# determine spectrum prefix

	prefix = ""
	for character in spectrum:
		if character == "_":
			break
		prefix = prefix + character

	# generate filenames

	back   = prefix + "_back_spec.pha"
	rmf    = prefix + "_src_spec.rmf"
	arf    = prefix + "_src_spec.arf"
	
	# overwriting or not

	if overwrite == True:
		over = '!'
	else:
		over = ''

	# generate grppha command

	command = 	'grppha ' + spectrum + ' ' + over + output + ' comm = "' + \
				'chkey BACKFILE ' + back + \
				' & chkey RESPFILE ' + rmf + \
				' & chkey ANCRFILE ' + arf + \
				' & ' + groupcommand + ' & exit"'

	# execute command

	os.system(command)


