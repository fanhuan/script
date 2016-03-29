#!/usr/bin/perl -w
#
# Author: Ruan Jue <ruanjue@gmail.com>
#
use strict;
use Getopt::Std;

our ($opt_h, $opt_n, $opt_d, $opt_l, $opt_j, $opt_f, $opt_o, $opt_M);

system("which kmer_count") and die("Cannot find kmer_count");
system("which filter") and die("Cannot find filter");

getopts("hf:d:l:j:o:n:M:");
&usage if($opt_h);
&usage unless($opt_d and -d $opt_d);
$opt_l = 25   unless($opt_l);
$opt_j = 1.0  unless($opt_j);
$opt_n = 1    unless($opt_n);
$opt_M = 4096 unless($opt_M);
$opt_f = 'FA' unless($opt_f);
$opt_o = "$opt_d/phylokmer.dat" unless($opt_o);

my @files;
my @clrs = ();

if($opt_f eq 'FA'){
	@files = split /\n/, `ls $opt_d/*.fa $opt_d/*.fasta`;
} else {
	@files = split /\n/, `ls $opt_d/*.fq $opt_d/*.fastq`;
}

die("None available files") unless(@files);

print "Program will process those files in 5 seconds\n";
print join("\n", @files);
print "\nKill me, if anything wrong\n";
sleep 5;

print "Create FIFO files\n";
foreach my $file (@files){
	die("There is already a fifo for $file, please check it.") if(-f "$file.fifo");
	`mkfifo $file.fifo`;
	push(@clrs, "rm $file.fifo");
}

die("There is already a fifo for $opt_o, please check it.") if(-f "$opt_o.fifo");
`mkfifo $opt_o.fifo`;
push(@clrs, "rm $opt_o.fifo");

my $cut_pid = &cut;

&filter;

&count;

while(my $pid = wait()){
	last if($pid == -1);
};

foreach my $clr (@clrs){
	system($clr);
}

1;

sub usage {
print <<EOF;
Usage: $0 [options]
Options
 -d <string> directory, contains all fasta files from one species
 -l <int>    kmer_size, default: 25
 -j <float>  jack-knife, default: 1.0
 -n <int>    minium frequency, default: 1
 -f <FA|FQ>  format of input files, default: FA
 -o <string> output, default: <-d>/phylokmer.dat
 -M <int>    memory limit, default: 4096(M)
 -h          show this document
EOF
exit;
}

sub cut {
	my $pid = fork;
	die("Cannot fork") if($pid == -1);
	if($pid == 0){
		my $n_unit = 3;
		my $n_file = @files;
		open(OUT, ">$opt_o") or die;
		open(IN, "$opt_o.fifo") or die;
		while(<IN>){
			my @tabs = split;
			my $num = 0;
			my $kmer = '';
			my $cpx  = '';
			for(my $i=0;$i<$n_file;$i++){
				next if($tabs[$i*$n_unit] eq '*');
				$kmer = $tabs[$i*$n_unit];
				$num += $tabs[$i*$n_unit+1];
				$cpx  = $tabs[$i*$n_unit+2];
			}
			print OUT "$kmer\t$num\t$cpx\n" if($num >= $opt_n);
		}
		close IN;
		close OUT;
		exit;
	}
	return $pid;
}

sub filter {
	my $pid = fork();
	die("Cannot fork\n") if($pid == -1);
	if($pid == 0){
		my $cmd = 'filter -k s -c -d "*" -a O,M,1 ' . join(" ", map {"$_.fifo"} @files) . " >$opt_o.fifo";
		system($cmd) and die("filter");
		exit;
	}
	return $pid;
}

sub count {
	foreach my $file (@files){
		my $pid = fork;
		die("Cannot fork") if($pid == -1);
		next if($pid);
		my $num = (split /\s+/, `wc -l $file`)[0];
		if($opt_f eq 'FA'){
			$num /= 2;
		} else {
			$num /= 4;
		}
		$num = int($num * $opt_j);
		my $cmd = qq{kmer_count -l $opt_l -f $opt_f -n 1 -M $opt_M -N $num -o $file.fifo -i $file};
		system($cmd);
		exit;
	}
}
