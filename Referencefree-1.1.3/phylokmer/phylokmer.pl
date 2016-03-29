#!/usr/bin/perl -w
#
#Author: Ruan Jue <ruanjue@gmail.com>
#
use warnings;
use Getopt::Std;

getopts("hsScl:d:o:n:N:M:f:j:");
&usage if(defined $opt_h or not defined $opt_d);
$opt_h = 0;
system("which kmer_count") and die("Cannot find kmer_count in PATH\n");
$opt_c and system("which kmer_cluster") and die("Cannot find kmer_cluster in PATH\n");
system("which filter") and die("Cannot find filter in PATH\n");

$opt_j ||= 1.0;
$opt_l ||= 25;
$opt_n ||= 0;
#$opt_N ||= 6;
$opt_M ||= 1024;
$opt_f ||= 'FA';
$opt_s ||= '';
$opt_S ||= '';
$opt_o ||= "$opt_d/phylokmer.dat";

die("Cannot find $opt_d\n") unless(-d $opt_d);

$| = 1;

my %dirs = ();
opendir(DIR, $opt_d) or die("Cannot open $opt_d");
while(my $file = readdir DIR){
	next if($file =~/^\.+$/);
	next unless(-d "$opt_d/$file");
	warn("Cannot opendir $opt_d/$file"),next unless(opendir(D, "$opt_d/$file"));
	while(my $f = readdir D){
		next if($f =~/^\.+$/);
		next if(-d "$opt_d/$file/$f");
		push(@{$dirs{$file}}, "$opt_d/$file/$f");
	}
	closedir D;
}
closedir DIR;

system "date";
print "FILE LIST:\n";
my @samples = ();
foreach my $dir (sort keys %dirs){
	my $fs = $dirs{$dir};
	my @files;
	if($opt_f eq 'FQ' or $opt_f eq 'fq'){
		@files = grep {m/\.fastq(\.gz)?$/i or m/\.fq(\.gz)?$/i} @$fs;
	} else {
		@files = grep {m/\.fasta(\.gz)?$/i or m/\.fa(\.gz)?$/i} @$fs;
	}
	next if(@files == 0);
	my $n_seq = 0;
	my $n_mer = 0;
	foreach my $file (@files){
		my ($n_line, $n_base) = ($opt_f eq 'fa' or $opt_f eq 'FA')? &stat_fa_file($file) : &stat_fq_file($file);
		$n_seq += $n_line;
		$n_mer += $n_base;
	}
	next if($n_seq == 0);
	$n_mer -= $n_seq * ($opt_l - 1);
	print "$dir\t$n_seq\t$n_mer\n";
	push(@samples, [$dir, [$n_seq, $n_mer], \@files]);
}

my $min_n = -1;
foreach my $sam (@samples){ $min_n = $sam->[1][1] if($min_n < 0 or $min_n > $sam->[1][1]); }

my $n_cutoff = int($min_n * $opt_j);
print "Number of kmers to be processed in every files: $n_cutoff\n";

my $cmd = qq{kmer_count -l $opt_l -f $opt_f -n $opt_n -M $opt_M};
$cmd .= qq{ -s} if($opt_s);
$cmd .= qq{ -S} if($opt_S);
foreach my $sample (@samples){
	my $command = $cmd;
	my $n_seq = int($n_cutoff / ($sample->[1][1] / $sample->[1][0]) + 0.5);
	$command .= " -N $n_seq -o '$opt_d/$sample->[0].pkdat'" . ($opt_c? " -r '$opt_d/$sample->[0].reads'" : "") . " -i '" . join("' -i '", @{$sample->[2]}) . "'";
	system "date";
	print "[CMD]: $command\n";
	system($command) and die("Error: $!");
	if($opt_c){
		$command = qq{kmer_cluster $opt_d/$sample->[0].pkdat $opt_d/$sample->[0].reads $opt_M > $opt_d/$sample->[0].clust};
		print "[CMD]: $command\n";
		system($command) and die("Error: $!");
	}
}

$cmd = qq{filter -k s -c -d '0' -a "T,M,1"};
for(my $i=0;$i<@samples;$i++){ $cmd .= " '$opt_d/$samples[$i][0].pkdat'"; }
$cmd .= " > $opt_o.raw";

system "date";
print "[CMD]: $cmd\n";
system($cmd) and die("Error: $!");
system "date";

open(IN, "$opt_o.raw") or die("Cannot open $opt_o.raw");
open(OUT, ">$opt_o") or die("Cannot write $opt_o");

print OUT "#-l $opt_l\n";
print OUT "#-n $opt_n\n";
print OUT "#-j $opt_j\n";
print OUT "#-s\n" if($opt_s);
print OUT "#-S\n" if($opt_S);
for(my $i=0;$i<@samples;$i++){ printf(OUT "#sample%d: %s\n", $i + 1, $samples[$i]->[0]); }

while(<IN>){
	chomp;
	my @tabs = split;
	my $kmer = '';
	for(my $i=0;$i<@tabs;$i+=2){
		if($tabs[$i]){ $kmer = $tabs[$i]; last; }
	}
	print OUT "$kmer";
	for(my $i=0;$i<@tabs;$i+=2){
		print OUT "\t", $tabs[$i+1];
	}
	print OUT "\n";
}

close IN;
close OUT;

open(OUT, ">$opt_o.cleanup.sh") or die("Cannot write $opt_o.cleanup.sh");
print OUT "#!/bin/sh\n";
print OUT "echo Cleanup\n";
print OUT "echo 'DEL: $opt_o.raw'\n";
print OUT "rm -f '$opt_o.raw'\n";
foreach my $s (@samples){
	print OUT  "echo 'DEL: $opt_d/$s->[0].pkdat'\n";
	print OUT "rm -f '$opt_d/$s->[0].pkdat'\n";
	print OUT  "echo 'DEL: $opt_d/$s->[0].reads'\n";
	print OUT "rm -f '$opt_d/$s->[0].reads'\n";
	print OUT  "echo 'DEL: $opt_d/$s->[0].clust'\n";
	print OUT "rm -f '$opt_d/$s->[0].clust'\n";
}
close OUT;
`chmod 755 $opt_o.cleanup.sh`;
print "Run $opt_o.cleanup.sh to clean temporary files\n";

1;

sub usage {
print qq{
phylokmer 1.4

Usage: $0 [options]
Options:
 -l integer  fragment length, default:25
 -n integer  threshold for minimum frequency, default: 0
 -s          turn on complexity filter
 -c          run kmer_cluster
 -d string   master directory containing the SRS data, organized by samples in subdirectories
 -f string   file format of input files, FA|FQ, default: FA
 -j float    (jack-knife) to what percentage should the original data be subsampled, default: 1.0
 -o string   output file, default: <-d>/phylokmer.dat
 -M mem_size memory limit, default: 1024

Require: kmer_count, kmer_cluster, filter

Result:
 col1: kmer
 col2: complexity
 col3: freqence in sample1
 ...
};
exit;
}

sub stat_fa_file {
	my $file = shift;
	my $n_line = 0;
	my $n_base = 0;
	if($file=~/\.gz$/){
		open(FILE, "gzip -dc $file |") or die("Cannot open $file");
	} else {
		open(FILE, $file) or die("Cannot open $file");
	}
	while(<FILE>){
		if(/^>/){
			$n_line ++;
		} else {
			$n_base += length($_) - 1;
		}
	}
	close FILE;
	return ($n_line, $n_base);
}

sub stat_fq_file {
	my $file = shift;
	my $n_line = 0;
	my $n_base = 0;
	if($file=~/\.gz$/){
		open(FILE, "gzip -dc $file |") or die("Cannot open $file");
	} else {
		open(FILE, $file) or die("Cannot open $file");
	}
	my $line = 0;
	while(<FILE>){
		next if(/^#/);
		if($line%4 == 1){
			$n_line ++;
			$n_base += length($_) - 1;
		}
		$line ++;
	}
	close FILE;
	return ($n_line, $n_base);
}

