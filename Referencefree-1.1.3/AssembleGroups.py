#! /usr/bin/python

from ReferenceFree.Pipeline import *
import os

def main( parser ):
	
	(option, args) = parser.parse_args()
	
	#check for command args
	allsteps = [ 'groupkmers', 'groupreads', 'groupassemble' ]
	option = setExecutablePaths( option )
	steps = setStepsArg( args, allsteps, option, parser )
	
	#check for shared kmer file
	requireOptions( [ 'shared' ], option, parser ) 
	
	#get parameters and make tag for file searching
	taxa, flags, params, paramtag = getSharedParamters( option.shared, option.metatag, '_' )
	
	#create directory for outputs if not exists
	if not option.groupoutdir:
		option.groupoutdir = os.path.join( os.path.dirname( option.shared ), 'Group_n{0}'.format( params['n'] ) )
	checkCreatePath( option.groupoutdir )
	
	#build pipeline
	stepfuncs = [ groups ]
	requiredopts = [] #[ 'ingroups' ]
	kwargs = { 'kmerpath': None, 'readpath': None }
	if 'groupkmers' in steps:	
		stepfuncs.append( groupkmers )
	if 'groupreads' in steps:
		requiredopts.append( 'readimportpath' )
		requireExecutable( option.RSpath )
		stepfuncs.append( groupreads )
	if 'groupassemble' in steps:
		requireExecutable( option.assembler )
		stepfuncs.append( groupassemble )
	requireOptions( requiredopts, option, parser )
	
	#run steps
	for func in stepfuncs:
		kwargs.update( func( option, parser, taxa, params, paramtag, **kwargs ) )

######################################################################################	

@trace
def groups( option, parser, taxa, params, paramtag, **kwargs ):
	'''Get ingroups for analysis'''
	ntaxa = len( taxa )
	ingroups = readGroups( option.ingroups ) if option.ingroups else makeIngroups( ntaxa )
	if max( chain( *ingroups ) ) >= ntaxa:
		raise ReferenceFreeError( "groups: Some group index in \'{0}\' is >= total number of samples in \'{1}\'"\
					.format( option.ingroups, option.shared ) )
	if min( chain( *ingroups ) ) < 0:
		raise ReferenceFreeError( "groups: Some group index in \'{0}\' is less than 1\n\tUse sample numbers from \'{1}\'"\
					.format( option.ingroups, option.shared ) )
	return { 'ingroups': ingroups }

@trace
def groupkmers( option, parser, taxa, params, paramtag, ingroups, **kwargs ):
	'''Generates group kmer files'''
	kmerpath = checkCreatePath( os.path.join( option.groupoutdir, 'kmers' ) )
	writeGroupKmers( ingroups, option.shared, params, kmerpath, option.quiet, option.exclusive ) 
	return { 'kmerpath': kmerpath }

@trace	
def groupreads( option, parser, taxa, params, paramtag, ingroups, kmerpath, **kwargs ):
	'''Extracts reads for groups'''
	#get in read files  
	try:
		inreadfiles = makeReadsDict( taxa, option.readimportpath )
	except OSError, msg:
		raise ReferenceFreeError( "groupreads: Error finding read files: {0}".format( msg ) )
	#check for readexportpath, create if not exists
	readpath = checkCreatePath( os.path.join( option.groupoutdir, 'reads' ) )
	if not option.quiet:
		prog = progress( "Extracting group reads...", sum( len(g) for g in ingroups ) )
		prog.print_msg()
	rsstdout = open( 'ReadsSelector_output', 'a' )
	try:
		if not kmerpath:
			kmerpath = os.path.join( option.groupoutdir, 'kmers' )
		inkmerfiles = getImportFiles( kmerpath )
	except OSError,msg:
		raise ReferenceFreeError( 'No group kmers found in {0}'.format( kmerpath ) )
	for n,group in enumerate( ingroups ):
		path = os.path.join( readpath, 'Group{0:03d}'.format( n ) )
		checkCreatePath( path )
		for tax in group:
			taxname = taxa[ tax ]
			kwgs = { "-s": inreadfiles[ taxname ] }
			ReadsSelector( option.RSpath, inkmerfiles[ n ], os.path.join( path, '{0:03d}_reads.fa.dat'.format( tax + 1 ) ) , rsstdout, **kwgs )
			if not option.quiet:
				prog.incr_val()
	if not option.quiet: prog.done()
	return { 'readpath': readpath }
	
@trace
def groupassemble( option, parser, taxa, params, paramtag, readpath, **kwargs ):
	'''pass extracted reads to an assembler'''
	#get extracted reads files
	if not readpath:
		readpath = os.path.join( option.groupoutdir, 'reads' )
	inreads = [ os.path.join( path,file ) for path,dirs,files in os.walk( readpath ) \
				for file in files if not file.startswith('.') ]
	if not inreads:
		raise ReferenceFreeError( 'No read files found in {0}'.format( readpath ) )
	
	#check for contig export path
	contigpath = checkCreatePath( os.path.join( option.groupoutdir, 'contigs' ) )
	
	#make output filenames and create paths
	ext = "contigs.dat"
	outcontigfiles = makeGroupContigOutfiles( inreads, contigpath, taxa, ext )
	
	#run assembler
	assembleReads( option.assembler, option.assemblekmerlength, inreads, outcontigfiles, configtemplate=option.assemblerconfig, \
		assembleroptions=option.assembleroptions, cleanfiles=option.cleanintermediates, quiet=option.quiet )
	
	return { 'contigpath': contigpath }
	
	
	

#########################################################################################

if __name__ == '__main__':
	from optparse import OptionParser

	parser = OptionParser()
	parser.add_option( "-s", "--shared", help="shared kmer file" )
	parser.add_option( "-g", "--ingroups", help="file with group tuples *NOTE: Python is zero-indexed* [default all pairwise groups]", default = '' )
	parser.add_option( "-e", "--exclusive", help="find kmers shared exclusively by group members [default kmers found in group genomes may also be found in non-members]", \
						default=False, action="store_true" )
	parser.add_option( "-x", "--groupoutdir", help="directory to store outputs. [default /sharedkmerpath/group_n#]", default = '' )
	parser.add_option( "-r", "--readimportpath", help="parent directory containing read data in subfolders named with convention \'SampleName1_SampleName2\'" )
	parser.add_option( "-A", "--assembler", help="name of assembler executable [default ABYSS]", \
						default="ABYSS" )
	parser.add_option( "-S", "--assemblerconfig", help="Configuration file for Assembler (e.g. SOAP) [default basic template, see README]", \
						default="" )
	parser.add_option( "-O", "--assembleroptions", help="Extra command-line options to pass to Assembler (in quotes e.g. \"-t 5 -c 3\")", \
						default="" )
	parser.add_option( "-C", "--cleanintermediates", help="Remove intermediates from assembly process (dep on assembler) [default True]", \
						default=True, action="store_false" )
	parser.add_option( "-k", "--assemblekmerlength", help="kmer length to pass to assembler program [default 21]", type="int", default='21' )
	parser.add_option( "-t", "--metatag", help="character in shared kmer file indicating meta data line [default #]", \
						default="#" )
	#parser.add_option( "-f", "--filenamesep", help="character used to separate parameters and genus/species in filename [default _]", \
	#					default="_" )
	parser.add_option( "-c", "--columnsep", help="character used to separate columns in kmer files [default \\t]", \
						default="\t")
	parser.add_option( "-q", "--quiet", help="run in quiet mode", \
						default=False, action="store_false" )
	
	parser.usage = '''%prog step -s /path/to/sharedfile -g /path/to/groupsfile [options] 
        
        \t\t\tMinimum arguments
        Extract kmers only:\t%prog groupkmers -s /path/to/sharedfile
        Extract reads only:\t%prog groupreads -s /path/to/sharedfile -r /path/to/reads
        Assemble reads only:\t%prog groupassemble -s /path/to/sharedfile  (extracted reads must exist in /sharedkmerpath/group_n#/reads/)
        Complete all steps:\t%prog all -s /path/to/sharedfile -r /path/to/reads
       
        Export path(s) will be created if not existing
        Note: ReadsSelector and Assembler executables (or symbolic link) must be in same path as %prog'''
	
	try:
		main( parser )
	except ReferenceFreeError, msg:
		print( '''\nError:\n{0}\nUse '-h' option to print help\n'''.format( msg ) )
		exit( 1 )
		
		
