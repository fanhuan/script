import os,sys,re,subprocess
from Bio import Entrez
from itertools import chain

#Change to enable_tracing=True to generate a debug tracing file

enable_tracing = False
if enable_tracing:
	debug_log = open( "ReferenceFree_debug_log", "w" ) 
else:
	debug_log = None

def trace( func ):
	'''Tracing decorator'''
	if enable_tracing:
		def callf( *args, **kwargs ):
			debug_log.write( "Calling: {0}: {1}, {2}\n\n".format( func.__name__, args, kwargs ) )
			r = func( *args, **kwargs )
			debug_log.write( "{0} returned {1}\n-----\n-----\n".format( func.__name__, r ) )
			return r
		return callf
	else:
		return func
		
def setExecutablePaths( option ):
	'''Sets paths to executables used in this analysis, in same path as this file'''
	option.RSpath = "./ReadsSelector"
	option.assembler = os.path.join( os.path.curdir, option.assembler )
	return option
	
def setStepsArg( args, allsteps, option, parser ):
	'''Check and format step arguments'''
	if not args:
		stepError( allsteps, option, parser )
	steps = args[0].lower()
	if not steps in allsteps + ['all']:
		stepError( allsteps, option, parser )
	if steps == 'all':
		steps = allsteps
	return steps

def getSharedParamters( sharedfile, metatag, filenamesep ):
	'''Read metadata from sharedkmer file'''
	taxa = getPKtaxa( sharedfile, metatag, sep=' ' )
	flags = [ "l","n","j" ]
	params = getParamdata( sharedfile, flags, metatag, sep=' ' )
	paramtag = makeParamtag( flags, [ params[ f ] for f in flags ], filenamesep )
	return ( taxa, flags, params, paramtag )

#Gets a list of all files in a directory, 'keyword' is a tag for a subset of the files, ie a set of parameters
@trace
def getImportFiles( path, keyword='' ):
	'''Find all files in a directory, with a keyword argument if supplied'''
	files = os.listdir( path )
	files = filter( lambda f: f.find( keyword ) != -1 and not f.startswith('.') and not os.path.isdir( f ), files )
	if not files:
		raise ReferenceFreeError( 'getImportFiles: No files returned in directory \'{0}\' with search keyword \'{1}\'.\nUse -A flag in command to use all files in import folder' \
						  .format( path, keyword if keyword else '' ) )
	files.sort()
	fullpathfiles = [ os.path.join( path, f ) for f in files ]
	return fullpathfiles
	
def checkCreatePath( path ):
 	'''Check a path to see if it exists, create if not'''
	if not os.path.exists( path ):
		os.makedirs( path )
	return path

def sharedkmergen( sharedkmerfile, metaTag='#', sep='\t' ):
	'''Generator for extracting data from sharedkmer file.  Memory-friendly, returns kmer and numeric list of taxa'''
	sharedstream = open( sharedkmerfile, 'r' )
	for line in sharedstream:
		if line.startswith( metaTag ): 
			continue
		linelist = line.rstrip( '\n' ).split( sep )
		sharedkmer = linelist.pop(0)
		taxa = [ taxnum for taxnum,kmers in enumerate(linelist) if kmers != '0' ]
		yield sharedkmer,taxa

def checkFileSorting( filelist, sharedtaxalist, namesep='_' ):
	'''This function makes sure that the files listed in a given filelist match samples in sharedkmer file'''
	for file,taxa in zip( filelist, sharedtaxalist ):
		if not getTaxaFromFilename( file, namesep ).upper() == taxa.upper():
			raise ReferenceFreeError( 'checkFileSorting: Shared taxa list mismatch starting with {0}'.format( taxa ) )

def getTaxaFromFilename( fullpathfilename, sep='_' ):
	'''Gets taxa name from file name, assumes format /path/to/file/genus[sep]species[sep]stuff.ext'''
	path,filename = os.path.split( fullpathfilename )
	file,ext = filename.split( '.' )
	return sep.join( file.split( sep )[:2] )

def getParamdata( sharedfile, flags=[ 'l','n','j' ], metaTag='#', sep=' ' ):
	'''Gets parameters from sharedkmer file'''
	try:
		f = open( sharedfile )
	except IOError,msg:
		print( str( msg ) )
		exit( -1 )
	cflags = list( flags )
	out = {}
	for line in f.xreadlines():
		if not cflags or not line.startswith( metaTag ): break
		flag,val = line.strip( metaTag + '-\n' ).split( sep )
		if flag in cflags:
			out[ flag ] = val 
			cflags.remove( flag )
	return out

def getPKtaxa( filename, metaTag='#', sep=' ' ):
	'''Returns list of taxa from shared kmer file'''
	sampleTag = 'sample'
	taxaPK = []
	f = open( filename )
	for line in f.xreadlines():
		if not line.startswith( metaTag ): break
		if line.startswith( metaTag + sampleTag ):
			taxaPK.append( line.strip( '\n' ).split( sep )[-1] )
	f.close()
	return taxaPK

def getFilebaseAndExtension( file ):
	'''splits filename into name.ext'''
	names = os.path.basename( file ).split('.')
	return ( names[0], names[-1] )

def makeFilename( writepath, paramlist, paramsep='_', filebase='', ext='.dat' ):
	'''general way to make filename'''
	params = paramsep.join( map( str, paramlist ) )
	return os.path.join( writepath, '.'.join( [ paramsep.join( [ filebase, params ] ), ext ] ) )
 
def makeIOlist( infilenamelist, outfilelist ):
	'''make list of input/output open filestreams'''
	return [ ( open( infile, 'r' ), open( outfile, 'w' ) ) for infile,outfile in zip ( infilenamelist, outfilelist ) ]
	
def makeParamtag( flags, vals, sep ):
	'''makes 'keyword' from parameters/flags for searching files eg 'l21_n3_j1' '''
	return sep.join( f+v for f,v in zip( flags,vals ) )

def requireOptions( names, option, parser ):
	'''checks for required arguments'''
	missing = [ name.upper() for name in names if not getattr( option, name ) ]
	if missing:
		plural = len( missing ) > 1
		raise ReferenceFreeError( "Mandatory argument{0} {1} {2} missing\n" \
				.format( "s" if plural else "", ','.join( missing ), "are" if plural else "is" ) )

def requireExecutable( expath ):
	'''checks for required executables'''
	if not os.access( expath, os.X_OK ):
		raise ReferenceFreeError( "Executable not located at {0}\n".format( expath ) )

def stepError( allsteps, option, parser ):
	'''raise an error if step argument incorrect'''
	raise ReferenceFreeError( "Argument [steps] must be one of {0}\n".format( ','.join( allsteps + ['all'] ) ) )
	
def closeIOlist( iolist ):
	'''closes a list of open file objects'''
	for sp in iolist:
		for stream in sp:
			stream.close() 

def file_len(fname):
	'''gets total length (lines) for file'''
	with open(fname) as f:
		for i, l in enumerate(f):
			pass
	return i + 1
	
def makeReadsDict( taxa, parentdir ):
	'''makes a dictionary taxa:[readfiles]'''
	return dict( ( tax, [ os.path.join( parentdir, tax, file ) \
				  for file in os.listdir( os.path.join( parentdir, tax ) ) ] ) \
				  for tax in taxa )

def ReadsSelector( RSpath, input_file1, output_filename, rsstdout, **kwargs ):
	'''Run ReadsSelector'''
	kwargs.update( { "-k": input_file1, "-o": output_filename } )
	callargs = [ RSpath ]
	for arg in kwargs.items():
		tup = [ ( arg[0], v ) for v in arg[1] ] if hasattr( arg[1], '__iter__' ) else [ arg ]
		[ callargs.extend( t ) for t in tup ]
	subprocess.check_call( callargs, stdout=rsstdout )
		
def write_to_file( fullpathfile, fields, datarows, sep='\t', header=None, append=False, overwrite=False ):
    '''Write lines of data to file

        Args:
        fullpathfile        :       Name of file to write to
        fields              :       List of column names
        datarows            :       List of lists/tuples--one list/tuple for each row of data, corresp to 'fields' above
        sep                 :       [optional] Field separator [ default = tab ]
        header              :       [optional] List of items for additional header (above field names, and inserted in pagebreaks) [ default = None ]
        append              :       [optional] If false, creates new file to write to, else appends to file of given name [ default = False ]
        overwrite           :       [optional] Overwrite existing files [ default = False ]
            
        Syntax:  write_to_file( '/path/to/filename.txt', ['id', 'name'], [[123, 'bob'],[456, 'dave'],[789,'Jill']], header=['date:','2007-7-7'] )
            
        Returns: Nothing'''
    mode = 'a' if append else 'w'
    if os.path.isfile( fullpathfile ) and mode=='w' and not overwrite:
            raise ReferenceFreeError( 'write_to_file: File {0} exists.  Set \'overwrite\' to True to overwrite'.format( fullpathfile ) )
    f = open( fullpathfile, mode )
    if header:
        f.write( sep.join( header ) + '\n' )
    if fields:
        f.write( sep.join( fields ) + '\n' )
    if datarows:
        for row in datarows:
            if row:
                f.write( sep.join( map( str, row ) ) + '\n' )
    f.close()

def textToPylist( infile, fields='All', header=True,  separator='\t', offset=None, limit=None ):
    '''This is an 'engine' for extracting data from text files.'''
    if not header and fields=='All':
        raise ReferenceFreeError( 'textToPylist: Fields parameter must be list of column names for header=False' )
    if type( infile )==str and os.path.isfile( infile ):
        ofile = open( infile )
        datalines = ofile.readlines()
        ofile.close()
    elif hasattr( infile, '__iter__' ):
        datalines = infile
    else:
        raise ReferenceFreeError( 'textToPylist: Cannot Import from {0}'.format( infile ) )
    alldata = map( lambda dat: dat.rstrip('\r\n').split( separator ), datalines )
    alldata = alldata[offset:limit]
    if header and len( alldata ) <= 1:
        raise ReferenceFreeError( 'textToPylist: Error Importing from\n\n{0}\n\nIs this saved in correct format?'.format( infile ) )
    datalist = []
    if header:
        allfields, data = alldata[0], alldata[1:]
        allfields = [ fld.strip( '"' ) for fld in allfields ]
    else:
        data = alldata
        allfields = fields
    if fields == 'All':
        usefields = allfields
    else:
        usefields = fields          
    datalist = [ [ ( datum + [''] * ( len(usefields) - len(datum) ) )[ allfields.index( field ) ].strip( '"' ) for field in usefields ] for datum in data ]
    return ( usefields, datalist )

def formatDerivedSharefilename( sharedfile, identifier, sep ):
	'''make filename for lineages/groups file'''
	return os.path.join( os.path.dirname(sharedfile), '{0}{sep}{identifier}.{1}'.format( *os.path.basename(sharedfile).split( os.path.extsep, 1 ), sep=sep, identifier=identifier ) )

@trace
def getLineage( genus, email, species=None ):
	'''Make list of lineages from NCBI using Biopython Entrez (queries require user's email address)'''
	db = 'taxonomy'
	if species:
		searchterm = ' '.join( [ genus, species ] )
	else:
		searchterm = genus
	searchterm += '[NAME]'
	idlist = getEntrezData( 'esearch', db, [ 'IdList' ], email, term=searchterm )[ 'IdList' ]
	nreturned = len( idlist )
	if not nreturned == 1:
		raise ReferenceFreeError( 'getLineage: {0} taxa returned from NCBI for search term: {1}'.format( 'No' if not nreturned else 'Multiple', searchterm ) )
	try:
		lineagefield = getEntrezData( 'efetch', db, ['Lineage'], email, id=idlist[0], rettype='xml', pars=entrezXMLhack( ['Lineage'] ) )[ 'Lineage' ]
	except KeyError,msg:
		raise ReferenceFreeError( 'getLineage: No Lineage data returned for {0}. Exiting.'.format( searchterm ) )
	return [ l.strip(' ') for l in lineagefield.split(';') ]

@trace	
def getEntrezData( tool, db, fields, email, pars=Entrez.read, **kwargs ):
	'''Get Data From NCBI using Entrez tools'''
	Entrez.email = email
	efunc = getattr( Entrez, tool )
	handle = efunc( db=db, **kwargs )
	result = pars( handle )
	return dict( ( k, result[k] ) for k in  fields )

@trace
def entrezXMLhack( fields ):
	'''For some reason, Entrez.efetch returns an html record for 'taxonomy', which Entrez won't parse (?).  This is a temp fix.'''
	brkt = dict( ( f, re.compile( '<{field}>(.*?)</{field}>'.format( field=f ) ) ) for f in fields )
	def p( handle ):
		result = handle.read()
		ret = {}
		for f,b in brkt.items():
			m = b.search( result )
			if m:
				ret[ f ] = m.group( 1 )
		return ret
	return p

@trace
def getAllLineages( filename=None, taxa=None, taxnamesep=' ', email=None, quiet=True ):
	'''Retrieve all lineages from either a file (exported by tools here) or from NCBI.  Ignores species names unless ambiguous genus name.'''
	if not filename and not taxa:
		raise ReferenceFreeError( 'getAllLineages: Come on!!  You have to pass SOME data for me to work with...!!' )
	if taxa and not email:
		raise ReferenceFreeError( 'getAllLineages: Entrez queries require an email address' )
	out = {}
	if filename:
		out = readLineages( filename )
	else:
		if not quiet:
			prog = progress( 'Retrieving lineages from NCBI (requests time-limited by external host)...', len( taxa ) )
			prog.print_msg()
		for tax in taxa:
			taxsplit = tax.split( taxnamesep )    
			try:
				lin = getLineage( taxsplit[0], email ) 
			except ReferenceFreeError, msg:
				if len( taxsplit ) > 1:
					lin = getLineage( taxsplit[0], email, species=taxsplit[1] )
				else:
					raise ReferenceFreeError( "getAllLineages: {0}".format( msg ) )
			out[ tax ] = lin
			if not quiet:
				prog.incr_val()
		if not quiet: prog.done()  
	return out    
	
def getAllGroupNodes( lineageslist ):
	'''Returns a list of the set of all unique names in all lineages in lineagelist'''
	return list( set( chain( *lineageslist ) ) )
	
def findLineages( node, lineagedict, minlins=2 ):
	'''returns tuple of sorted names having given node and list length >=minlins'''
	lineages = [ k for k,v in lineagedict.items() if node in v ]
	lineages.sort()
	return tuple( lineages ) if len( lineages ) >= minlins else None

def makeGroupsList( lineagedict, allnodes ):
	'''returns list of tuples containing names of groups sorted by nodes'''
	groups = [ findLineages( node, lineagedict ) for node in allnodes ]
	return list( set( filter( lambda g: g, groups ) ) )
		
def getGroupsSortOrder( groups, alltaxa ):
	'''returns list of tuples, each containing the sorted order number of the taxa'''
	alltaxa= sorted( alltaxa )
	groupsnum = [ tuple( alltaxa.index( tax ) for tax in group ) for group in groups ]
	return sorted( groupsnum )

def writeLineages( lineage, filename ):
	write_to_file( filename, [], [ ( k, ','.join(v) ) for k,v in lineage.items() ], overwrite=True )

def readLineages( filename ):
	fields,data = textToPylist( filename, fields=['taxa','lineage'], header=False )
	return dict( ( k, v.split( ',' ) ) for k,v in data )
	
def writeGroups( ingroups, filename ):
	write_to_file( filename, [], [ (g,) for g in map( str, ingroups ) ], overwrite=True )

def readGroups( filename ):
	fields,data = textToPylist( filename, fields=['groups'], header=False )
	return [ eval(g[0]) for g in data ]
	
@trace
def writeGroupKmers( numberedgroups, sharedkmerfile, params, kmerpath, quiet=True, **kwargs ):
	'''Write kmers to subfolder'''
	kmerfiles = dict( ( group, open( os.path.join( kmerpath, 'Group{0:03d}_{1}mers.dat'.format( n, params['l'] ) ), 'w' ) )\
		                   for n,group in enumerate( numberedgroups ) )
	sharedkmers = sharedkmergen( sharedkmerfile, metaTag='#', sep='\t' )
	if not quiet:
		msg = 'Generating group kmer files'
		prog = progress( msg, file_len( sharedkmerfile ) )
		prog.print_msg()
	for kmer,gwithkmer in sharedkmers:
		for group in numberedgroups:
			if all( g in gwithkmer for g in group ):
				kmerfiles[ group ].write( kmer + '\n' )
		if not quiet:
			prog.incr_val()
	if not quiet: prog.done()
	
@trace
def makeIngroups( lineage ):
	'''returns list of tuples (numericgroups)'''
	allnodes = getAllGroupNodes( lineage.values() )
	groups = makeGroupsList( lineage, allnodes )
	groupsnum = getGroupsSortOrder( groups, lineage.keys() ) 
	return groupsnum

@trace
def makeGroupContigOutfiles( inreads, outdir, taxa, ext ):
	'''makes filenames and makes sure directories exist'''
	out = []
	for file in inreads:
		dir,filename = os.path.split( file )
		taxon = taxa[ int( filename.split('_')[0] ) ]
		group = os.path.split( dir )[-1]
		outfilename = makeFilename( os.path.join( outdir, group ), [ group ], filebase=taxon, ext=ext )
		checkCreatePath( os.path.dirname( outfilename ) )
		out.append( outfilename )
	return out

def writeUntilFound( sharedkmer, streampair, sep='\t' ):
	'''write lines from stream one to stream two until reaching the shared read'''
	try:
		line = streampair[0].next()
		while not line.split( sep )[0] == sharedkmer:
			streampair[1].write( line )
			line = streampair[0].next()
	except StopIteration:
		pass

def writeTypeIkmers( sharedkmerfile, inkmerfiles, outkmerfiles, paramsep='_', maxfiles=100, metaTag='#', sep='\t', quiet=True ):
	'''Extract TypeI kmers using shreadkmer file and kmer files from taxa'''
	if not quiet: 
		filelen = file_len( sharedkmerfile ) 
		prog = progress( "Writing kmer files %d to %d...", filelen )
	sharedtaxa = getPKtaxa( sharedkmerfile )
	checkFileSorting( inkmerfiles, sharedtaxa, paramsep )
	totalfiles= len( inkmerfiles )
	setnumber = 0
	while inkmerfiles:
		partialinlist,inkmerfiles = inkmerfiles[:maxfiles],inkmerfiles[maxfiles:]
		partialoutlist,outkmerfiles = outkmerfiles[:maxfiles],outkmerfiles[maxfiles:]
		setnumber += 1
		if not quiet:
			prog.reset()
			prog.print_msg( *[(setnumber - 1)*maxfiles + 1, min(setnumber*maxfiles, totalfiles ) ] )
		iolist = makeIOlist( partialinlist, partialoutlist )
		for sharedkmer,taxalist in sharedkmergen( sharedkmerfile, metaTag, sep ):
			if not quiet:
				prog.incr_val()
			startidx,stopidx = (setnumber - 1)*maxfiles, setnumber*maxfiles
			partialidxlist = range( startidx, stopidx )
			for taxa in taxalist:
				if taxa in partialidxlist:
					writeUntilFound( sharedkmer, iolist[taxa - startidx], sep )
		[ writeUntilFound( '', sp, sep ) for sp in iolist ]
		closeIOlist( iolist )
	if not quiet: prog.done()

@trace
def extractTypeIreads( RSpath, inkmerfiles, inreadfiles, outreadfiles, convertfq2fa=True, quiet=True ):
	'''Extract TypeI reads using kmer files and read files from taxa'''
	if not quiet:
		numtaxa = len( inkmerfiles )
		prog = progress( "Extracting reads...", numtaxa )
		prog.print_msg()
	stdoutfile = "ReadsSelector_output"
	rsstdout = open( stdoutfile, 'a' )
	for kmerfile in inkmerfiles:
		tax = getTaxaFromFilename( kmerfile )
		kwargs = { "-s": inreadfiles[ tax ] }
		if convertfq2fa: kwargs[ "-fa" ] = ""
		ReadsSelector( RSpath, kmerfile, outreadfiles[ tax ], rsstdout, **kwargs )
		if not quiet:
			prog.incr_val()
	rsstdout.close()
	#os.remove ( stdoutfile )
	if not quiet: prog.done()

@trace
def Assembler( assemblerpath, kmerlength, infiles, outfile, assemstdout, **kwargs ):
	'''Run assembler (ABYSS)'''
	kwargs.update( { "-k": kmerlength, "-o": outfile } )
	callargs = [ assemblerpath ]
	for arg in kwargs.items():
		callargs.extend( arg )
	addf = callargs.extend if hasattr( infiles, '__iter__' ) else callargs.append
	addf( infiles )
	try:
		subprocess.check_call( callargs, stdout=assemstdout, stderr=assemstdout )
	except subprocess.CalledProcessError, msg:
		sys.stdout.write( "\b\b\b\nError returned for call: %s\n%s\n   " \
						  % ( ' '.join( callargs ), "See %s_output for more info" \
						  % os.path.basename( assemblerpath ) ) )

@trace
def assembleReads( assemblerpath, kmerlength, inreadfiles, outcontigfiles, quiet=True ):
	'''Loop through sets to pass to assembler'''
	if not quiet:
		prog = progress( "Assembling reads...", len( inreadfiles ) )
		prog.print_msg()
	stdoutfile = "%s_output" % os.path.basename( assemblerpath )
	assemstdout = open( stdoutfile, 'a' )
	for infile,outfile in zip( inreadfiles, outcontigfiles ):
		Assembler( assemblerpath, kmerlength, infile, outfile, assemstdout )
		if not quiet:
			prog.incr_val()
	assemstdout.close()
	if not quiet: prog.done()
	
class progress:
	'''progress tracker'''
	def __init__( self, message, maxval ):
		self.message = message
		self.percentlist = [ int( p*maxval/100 ) for p in range(100) ]
		self.val = 1
		self.percent = 0
	def print_msg( self, *args ):
		sys.stdout.write( "\n%s\n" % ( self.message if not args else self.message % args ) )
		sys.stdout.flush()
	def incr_val( self ):
		self.val += 1
		if self.val in self.percentlist:
			self.percent = self.percentlist.index( self.val )
			sys.stdout.write( "\b\b\b%2d%%" % self.percent )
			sys.stdout.flush()
	def done( self ):
		sys.stdout.write( "\nDone\n" )
	def reset( self ):
		self.val = 1
		self.percent = 0

class ReferenceFreeError( Exception ):
    '''Error class for general errors from this "module"'''
    def __init__( self, value ):
        self.value = value
    def __str__( self ):
        return str( self.value )
    def __repr__( self ):
        return str( self.value )
        
