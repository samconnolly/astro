# tcl macro to run on spectra
tclmacro = \
'puts "Starting macro..."\n\
@{0}\n'.format(infile)

if modelfile:

	tclmacro = tclmacro + '@{0}\n'.format(modelfile)

tclmacro = tclmacro + \
'query yes \n\
fit \n\
set outfile [open {0} w]\n\
tclout datagrp\n\
set grpnum $xspec_tclout\n\
puts $outfile $grpnum\n'.format(tmpfilegrpnum)

tclmacro = tclmacro + \
'set i 1\n\
while {$i <= $grpnum} {;\n'

tclmacro = tclmacro + \
'puts "spectrum $i of $grpnum$"\n\
set outfile [open {0}$i.dat w]\n\
tclout energies $i\n\
puts $outfile $xspec_tclout\n\
set outfile [open {1}$i.dat w]\n\
tclout modval $i\n\
puts $outfile $xspec_tclout \n\
set outfile [open {2}$i.dat w]\n\
tclout noticed energy $i\n\
puts $outfile $xspec_tclout \n'\
.format(tmpfileenergy,tmpfilevalue,tmpfilenotice)

tclmacro = tclmacro + \
'; incr i;} \n\
quit\n'

#print tclmacro

# create temporary macro file
macrofile= open(macrolocation, 'w')
macrofile.write(str(tclmacro))
macrofile.close()

# run tcl script in xspec
os.chdir(route)
os.system("xspec - tmpmacro.tcl")

# delete temporary macro
os.remove(macrolocation)
