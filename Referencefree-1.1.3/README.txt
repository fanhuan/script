Inside the tar file:
AssembleTypeI.py
AssembleGroups.py
ReferenceFreeSource (directory)
	ReferenceFree package
	ReadsSelector.cpp
phylokmer (directory)
	various, see below

ReferenceFreeSource is the package containing code for both Python applications. (Author: John Harting)
AssembleTypeI.py is an application for creating TypeI contigs. (Author: John Harting)
AssembleGroups.py is an application for creating group contigs. (Author: John Harting)
ReadsSelector.cpp is the C++ source for ReadsSelector (Author: Ye Chengxi)
phylokmer is a directory containing several programs (C, Perl) for creating shared kmer files (Author: Jue Ruan)


Dependencies:
Perl
Python 2.6 and higher 2.X versions  (NOT Python 3.0+).
g++/gcc compilers
ABySS or SOAPdenovoXXXmer


Installation:

(1.) Unpack into some directory and cd into that directory

(2.) Compile ReadsSelector.

g++ ReferenceFreeSource/ReadsSelector.cpp -o ReadsSelector

(3.) Compile phylokmer programs (used to build shared kmer files).

cd phylokmer
make 

**A switch on the gcc compiler for Ubuntu 11.10 causes an error on make.  See http://stackoverflow.com/questions/7824439/c-math-linker-problems-on-ubuntu-11-10.  

(4.) Add phylokmer folder to execute path.

PATH=/path/to/phylokmer:${PATH}
export PATH

(5.)  Get an Assembler.  ABYSS and SOAP are supported as of version 1.1.1. 

ABYSS:

Get ABySS at http://www.bcgsc.ca/platform/bioinfo/software/abyss.  As of 9/13/12, ABySS is available for Ubuntu Linux users through the repository (apt-get).  For OSX users, you will need to compile from source (unless you wish to use ABySS 1.3.3, which has an installer but see release 1.3.4 notes for issues with that version).  Install following the instructions provided on the web site. 

Following installation, add a symbolic link from the ABySS executable to the directory where the python applications are, /ReferenceFree.  If the ABYSS binary is located in /myabyssdir, 

ln -s /myabyssdir/ABYSS /path/to/ReferenceFree/ABYSS

If the ABySS path was added to the executable PATH on installation, the link can be made with the command:

ln -s `which ABYSS` /path/to/ReferenceFree/ABYSS

where the tick marks are backquotes (on tilde key).  

SOAP:

Get desired SOAPdenovoXXXmer executable from http://soap.genomics.org.cn/soapdenovo.html by downloading and unpacking the tar ball in some directory, e.g. /mysoapdir.  There are three different versions, depending on max kmer length (31,63,127).  Any of the three will work with the ReferenceFree pipeline and can be used interchangeably simply by pointing the SOAP link to the desired original binary file.  After you have unpacked the SOAPdenovoXXXmer.tar package, make sure that the binary file inside is executable--the result of the command 'ls -l /mysoapdir' should have x's in the file permissions string similar to the following:

-rwxr-xr-x@ 1 User  staff  245512 Feb 13  2011 SOAPdenovo31mer

Next, add a symbolic link to the SOAPdenovoXXXmer executable named SOAP (just SOAP) to the directory where the python applications are, /ReferenceFree.

ln -s /mysoapdir/SOAPdenovo31mer /path/to/ReferenceFree/SOAP

*****See below for more information on switching assemblers, passing options, and using SOAP configuration files for assembly*****


(6.) Install the ReferenceFree package into python.

cd ReferenceFreeSource
sudo python setup.py install

**If you do not have admin access and/or want to set up a virtual python interpreter with local package directory (e.g. on a university computing grid), you can follow the steps below which will set up in /mydirectory (see http://pypi.python.org/pypi/virtualenv for more info).  If you are running this on a Mac and you do not have 'wget' installed, simply replace it with 'curl -O'.:

wget https://raw.github.com/pypa/virtualenv/master/virtualenv.py
python virtualenv.py /mydirectory
source /mydirectory/bin/activate
cd /path/to/ReferenceFreeSource
python setup.py install


Then, when you execute AssembleTypI.py and/or AssembleGroups.py, make sure you invoke the virtual python interpreter just created.  After executing the 'source' command above, the prompt should have changed such that '(mydirectory)' appears in the prompt.  This means that the virtual python interpreter there is invoked when the command 'python' is used to execute python scripts.  If you open a new command line terminal, however, the default python interpreter is activated.  Execute the 'source' command line again to activate the virtual python interpreter.  This can also be made into an alias to put in your .bash_profile.

echo 'alias reffree="source /mydirectory/bin/activate"' >> ~/.bash_profile



 

-----------------SOME PHYLOKMER HELP--------------------------------------------------

Phylokmer and building the shared kmer file:

Help menus for phylokmer programs can be displayed by typing the executable name at the terminal.  The following is an example set of commands to create a shared kmer file for analysis and also move the individual output pkdat files into a directory separate from the original reads directory:


perl /path/to/phylokmer/phylokmer.pl -l 21 -n 3 -d /path/to/sequence_data -f FA -j 1 -o /path/to/outputdata/pkdat/somegroupname_l21_n3_j1.shared.pkdat
mkdir /path/to/outputdata/pkdat/somegroupname/
mv /path/to/outputdata/pkdat/*pkdat /path/to/outputdata/pkdat/somegroupname/


NOTE:  The /path/to/sequence_data directory should contain directories of fa/fq files for each taxa/sample.  The sample names created inside the file named in the '-o' argument will match the directory names and should not be changed, otherwise the applications downstream will be unable to match data in the pipeline.

Two additional files will also be created, a '.cleanup.sh' file and '.raw' file.  These files are unused in this pipeline and can be ignored or removed.    




-----------------HELP FOR (SOME) ASSEMBLE*.PY COMMAND OPTIONS--------------------------

Help menus for both Python applications can be displayed by the following at the terminal:

python AssembleTypeI.py -h
python AssembleGroups.py -h

There are lots of options, but most of them have 'reasonable' defaults.  Each help menu has a set of 'minimum' arguments to run the steps in the applications.  Assuming you already have your shared kmer file and reads available, a basic run of one of the programs completing all steps would use the commands (make sure to include the steps argument, immediately after the application python file):

AssembleTypeI:


python AssembleTypeI.py all -s /path/to/sharedkmerfile -i /path/to/kmer/dir -r /path/to/reads/dir 


AssembleGroups:


python AssembleGroups.py all -s /path/to/sharedfile -r /path/to/reads/dir


Note that the default 'groups' are all pair-wise combinations of the input samples.  To define other groups, create a text file with numeric tuples, one each line, defining the groups by their sample numbers in the shared kmer file.  For example, if the top few lines of your shared file look like:

#-l 21
#-n 3
#-j 1
#sample1: Acidosasa_purpurea
#sample2: Ageratina_adenophora
#sample3: Angiopteris_evecta
#sample4: Bambusa_oldhamii

and you wish to extract kmers shared by the groups ( Acidosasa_purpurea, Ageratina_adenophora ) and ( Ageratina_adenophora, Angiopteris_evecta, Bambusa_oldhamii ), create a file /mygroupdir/groups.txt with two lines:

(1,2)
(2,3,4)


Then pass that file to the AssembleGroups.py application with the '-g' flag:


python AssembleGroups.py all -s /path/to/sharedfile -r /path/to/reads/dir -g /mygroupdir/groups.txt


Any number of groups and samples within groups can be passed this way via the '-g' groups file.  One additional option also affects how group kmers are extracted.  By default, 'group kmers' include any kmer which is found in all the samples of a given group AND MAY ALSO BE FOUND IN OTHER SAMPLES.  To extract group kmers which are found in all members of a group and ONLY in those members (i.e. ABSENT IN ALL OTHER SAMPLES included in the shared kmer file), use the '-e' flag (exclusive).



Each step in both pipelines can take a little while, depending on the dataset size, so its also possible to run steps independently by setting the 'steps' argument and passing the appropriate options (see help). 

Data outputs go to the specified or generated directories (see options), and also stdout and stderror outputs from ReadsSelector/Assembler are captured and put in respective text files in the folder containing the application files. 


***General ASSEMBLER instructions***:

As of this version, all data from fq read files will be converted to fa by the ReadsSelector before the final assembly step.  This may change in the future.

The default assembler is ABYSS--if the '-A' argument is not passed to the Assemble*.py apps, they will look for the ABYSS link in the app directory and pass all arguments to it.

To pass arbitrary (but see below) command-line arguments to the assembler, pass them as an argument to the '-O' option IN QUOTES.  For example, to trim dangling edges and remove low-coverage contigs using ABYSS, you would use the command:


python AssembleTypeI.py all -s /path/to/sharedkmerfile -i /path/to/kmer/dir -r /path/to/reads/dir -O "-t 4 -c 3"


*Note that some arguments (e.g. kmer length and minimum assembler arguments) are automatically passed to the assembler by the pipeline.  If you want to use a specific kmer length other than the ReferenceFree default (21), you should use the '-k' flag directly in the Assemble*.py command, i.e.:

python AssembleTypeI.py all -s /path/to/sharedkmerfile -i /path/to/kmer/dir -r /path/to/reads/dir -k 23

Duplicate arguments passed via the '-O' option will throw warnings, but not stop the process.


ABYSS specific instructions:

ABYSS is the default, so it is not necessary to use '-A ABYSS' to use it.  No intermediate files are produced, so using the '-C' flag has no effect.  ABySS does not take a configuration file, so the -S argument will also be ignored.


SOAP specific instructions:

The ReferenceFree pipeline (at this time) will only use a single read library (output from ReadsSelector) for SOAP assembly, and will only complete the first two steps (pregraph and contig) of the SOAP pipeline.  To use the SOAPdenovoXXXmer assembler(s), you must add (at the minimum) '-A SOAP' to the command:

python AssembleTypeI.py all -s /path/to/sharedkmerfile -i /path/to/kmer/dir -r /path/to/reads/dir -A SOAP

Options/Configuration for the SOAPdenovo assembler come in two flavors:  

1. Command-line options -- passed to SOAP via the '-O' option as above.  

2. Configuration file

A config file can be passed to SOAP via the '-S' flag.  A file passed this way will be used as a template for all assemblies and may contain general and library parameter specifications.  See the SOAP page for more information on which parameters can be used.  If your template is /mysoapdir/SOAPconfig.txt, it can be a text file with only general parameters:

param1=value1
param2=value2

or it may also include library parameters:

param1=value1
param2=value2
[LIB]
libparam1=libvalue1

Either format is fine, but make sure NOT to add file locations for reads (f/q parameters).  Those parameters will be added to the template by the ReferenceFree pipeline for each sample (thus the '/mysoapdir/SOAPconfig.txt' file is just a template).  At some future point, we may add the ability to run the map/scaffold steps with additional read libraries.  A sample command would be like:


python AssembleTypeI.py all -s /path/to/sharedkmerfile -i /path/to/kmer/dir -r /path/to/reads/dir -A SOAP -S /mysoapdir/SOAPconfig.txt


If no user-specified SOAP config file is provided, the ReferenceFree pipeline uses a very (very) basic template with only a single parameter (max_rd_len=51).  This template will appear in the application folder at the beginning of the assembly run.  

The SOAP assembler creates several intermediate files during processing, all of which are removed by default except the .contig outputs.  To prevent cleanup of these files (e.g. to see specific config files for any given run of the assembler), use the '-C' flag in the command above.     












 
