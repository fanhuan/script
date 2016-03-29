#! /usr/bin/python

from ReferenceFree.Pipeline import *
import os,sys,subprocess

		
#main loop
def main( parser ):
	
	(option, args) = parser.parse_args()
	
	allsteps = [ 'kmers', 'reads', 'assemble' ]
	option = setExecutablePaths( option )
	steps = setStepsArg( args, allsteps, option, parser )

	#check for required "options" and build pipeline
	required = [ "shared" ] 
	stepfuncs = []
	
	if 'kmers' in steps:
		required.append( "kmerimportpath" )
		stepfuncs.append( kmers )
	if 'reads' in steps:
		required.append( "readimportpath" )
		if not 'kmers' in steps:
			required.append( "kmerexportpath" ) 
		requireExecutable( option.RSpath )
		stepfuncs.append( reads )
	if 'assemble' in steps:
		if not 'reads' in steps:
			required.append( "readexportpath" )
		requireExecutable( option.assembler )
		stepfuncs.append( assemble )
	requireOptions( required, option, parser )
        
	#get parameters and make tag for file searching
	taxa, flags, params, paramtag = getSharedParamters( option.shared, option.metatag, '_' )  
	
	#run all steps
	returnvals = {}
	for func in stepfuncs:
		returnvals.update( func( option, taxa, params, paramtag, **returnvals ) )

@trace
def kmers( option, taxa, params, paramtag, **kwargs ):
	'''extract TypeI kmers using shared kmer file and reads files'''
	#get files with the right paramter tag
	try:
		inkmerfiles = getImportFiles( option.kmerimportpath, paramtag if option.filter else '' )
	except ValueError, msg:
		raise ReferenceFreeError( "kmers function: {0}".format( msg ) )

	#make kmerexportpath variable if not given
	if not option.kmerexportpath:
		option.kmerexportpath = os.path.join( option.kmerimportpath, os.path.pardir, "TypeI_n" + params["n"], "kmers" ) 

	#create kmerimportpath directory if not exists
	checkCreatePath( option.kmerexportpath )

	#make list of output filenames
	outkmerfilenames = [ makeFilename( option.kmerexportpath, [ "TypeI" ], '_', \
						**dict( zip( [ "filebase", "ext" ], getFilebaseAndExtension( infile ) ) ) ) \
						for infile in inkmerfiles ]

	#run kmer extraction
	try:
		writeTypeIkmers( option.shared, inkmerfiles, outkmerfilenames, '_', \
						 option.maxfiles, option.metatag, option.columnsep, option.quiet )
	except ValueError, msg:
		raise ReferenceFreeError( "writeTypeIkmers: {0}".format( msg ) )
	return { "outkmerfilenames" : outkmerfilenames }

@trace
def reads( option, taxa, params, paramtag, **kwargs ):
	'''Run ReadsSelector over extracted TypeIkmers to get reads from read files'''
	#get in kmerfiles
	try:
		inkmerfiles = outkmerfilenames
	except NameError, msg:
		inkmerfiles = getImportFiles( option.kmerexportpath, paramtag if option.filter else '' ) 

	#get in read files  
	try:
		inreadfiles = makeReadsDict( taxa, option.readimportpath )
	except OSError, msg:
		raise ReferenceFreeError( "Reads function: Cannot find read files: {0}".format( msg ) )

	#check for readexportpath, create if not exists
	if not option.readexportpath:
		option.readexportpath = os.path.join( option.kmerexportpath, os.path.pardir, "reads" )
	checkCreatePath( option.readexportpath )

	#make out filenames
	#(hole in logic)
	ext = "fa.dat"
	outreadfiles = dict( ( tax, makeFilename( option.readexportpath, [ "TypeI%sreads" % params["l"] ], \
						  '_', tax, ext ) ) \
						  for tax in taxa )

	#run selector
	extractTypeIreads( option.RSpath, inkmerfiles, inreadfiles, outreadfiles, option.quiet )
	
	return { "outreadfiles" : outreadfiles }
	
@trace
def assemble( option, taxa, params, paramtag, **kwargs ):
	'''Assemble extracted reads into TypeI contigs'''
	#get in reads files
	try:
		readimportfiles = outreadfiles.values()
	except NameError,msg:
		keyword = '' if not option.filter else "TypeI%sreads.fa.dat" % params["l"]
		readimportfiles = getImportFiles( option.readexportpath, keyword )
		
	#check for contigexportpath, create if not exists
	if not option.contigexportpath:
		option.contigexportpath = os.path.join( option.readexportpath, os.path.pardir, "contigs" )
	checkCreatePath( option.contigexportpath )

	#make out filenames
	ext = "contigs.dat"
	outcontigfiles = [ makeFilename( option.contigexportpath, [ "TypeI%s" % params["l"] ], \
					  '_', tax, ext ) \
					  for tax in taxa ]

	#run assembler
	assembleReads( option.assembler, option.assemblekmerlength, readimportfiles, outcontigfiles, configtemplate=option.assemblerconfig, \
					assembleroptions=option.assembleroptions, cleanfiles=option.cleanintermediates, quiet=option.quiet )

	return { "outcontigfiles" : outcontigfiles }



#########################################################################################


if __name__ == '__main__':
	from optparse import OptionParser

	parser = OptionParser()
	parser.add_option( "-s", "--shared", help="shared kmer file" )
	parser.add_option( "-i", "--kmerimportpath", help="directory containing individual taxa kmer files" )
	parser.add_option( "-F", "--filter", help="filter files  in kmer directory by parameters [default all files in directory]", \
						default=False, action="store_true" )
	parser.add_option( "-e", "--kmerexportpath", help="directory to export TypeI kmers [default /kmerimportpath/../TypeI_n#/kmers/]", \
						default='' )
#	parser.add_option( "-a", "--convertfq2fa", help="convert .fq reads to .fa [default: True]", \
#						default=True )
	parser.add_option( "-r", "--readimportpath", help="parent directory containing read data in subfolders named by taxa" )
	parser.add_option( "-x", "--readexportpath", help="directory to export extracted reads [default /kmerexportpath/../reads]", \
						default='' )
	parser.add_option( "-A", "--assembler", help="name of assembler executable [default ABYSS]", \
						default="ABYSS" )
	parser.add_option( "-c", "--contigexportpath", help="directory to export assembled contigs [default /readexportpath/../contigs]", \
						default='' )
	parser.add_option( "-S", "--assemblerconfig", help="Configuration file for Assembler (e.g. SOAP) [default basic template, see README]", \
						default="" )
	parser.add_option( "-O", "--assembleroptions", help="Extra command-line options to pass to Assembler (in quotes e.g. \"-t 5 -c 3\")", \
						default="" )
	parser.add_option( "-C", "--cleanintermediates", help="Remove intermediates from assembly process (dep on assembler) [default True]", \
						default=True, action="store_false" )
	parser.add_option( "-k", "--assemblekmerlength", help="kmer length to pass to assembler program [default 21]", type="int", default='21' )
	parser.add_option( "-m", "--maxfiles", help="maximum files to search at one time [default 100]", type="int",\
						default=100 )
	parser.add_option( "-t", "--metatag", help="character in shared kmer file indicating meta data line [default #]", \
						default="#" )
	parser.add_option( "-l", "--columnsep", help="character used to separate columns in kmer files [default \\t]", \
						default="\t")
	#parser.add_option( "-f", "--filenamesep", help="character used to separate parameters and genus/species in filename [default _]", \
	#					default="_" )
	parser.add_option( "-q", "--quiet", help="run in quiet mode", \
						default=False, action="store_false" )

	parser.usage = '''%prog [steps] [arguments]
	
        \t\t\tMinimum arguments
        Extract kmers only:\t%prog kmers -s /path/to/sharedfile -i /path/to/kmer/dir
        Extract reads only:\t%prog reads -s /path/to/sharedfile -e /path/to/TypeIkmers -r /path/to/reads
        Assemble reads only:\t%prog assemble -s /path/to/sharedfile -x /path/to/TypeIreads
        Complete all steps:\t%prog all -s /path/to/sharedfile -i /path/to/kmer/dir -r /path/to/reads
       
        Export path(s) will be created if not existing
        Note: ReadsSelector and Assembler executables (or symbolic link) must be in same path as %prog'''
	
	try:
		main( parser )
	except ReferenceFreeError, msg:
		print( '''\nError:\n{0}\nUse '-h' option to print help\n'''.format( msg ) )
		#parser.print_help()
		exit( 1 )

 
