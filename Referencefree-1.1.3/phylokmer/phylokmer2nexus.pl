#!/usr/bin/perl -w
#
#Author: Ruan Jue <ruanjue@gmail.com>
#
use warnings;
use Getopt::Std;

getopts("hn:s:i:o:");
&usage if(defined $opt_h or not defined $opt_i or not defined $opt_o);
$opt_h = 0;
$opt_n ||= 6;
$opt_s ||= 200;

my $off = 1;

open(IN, $opt_i) or die("Cannot open $opt_i");
open(OUT, ">$opt_o") or die("Cannot write $opt_o");
my @data = ();
my @samples = ();
while(<IN>){
	chomp;
	if(/^#sample(\d+):\s+(.+)/){
		$samples[$1-1][0] = $2;
		$data[$1-1] = '';
		next;
	}
	my @tabs = split;
	next unless(@tabs == @samples + 2);
	next if($tabs[1] < $opt_s);
	my $n_one = 0;
	my $n_zero = 0;
	for(my $i=0;$i<@samples;$i++){
		if($tabs[$off+$i] >= $opt_n){
			$tabs[$off+$i] = '1';
			$n_one ++;
		} elsif($tabs[$off+$i] == 0){
			$tabs[$off+$i] = '0';
			$n_zero ++;
		} else {
			$tabs[$off+$i] = '?';
		}
	}
	next if($n_one <= 1 or $n_zero < 1);
	for(my $i=0;$i<@samples;$i++){
		$data[$i] .= $tabs[$off+$i];
	}
}
close IN;
my $n_sam = @samples;
my $n_chs = length($data[0]);
print OUT qq{#NEXUS\n};
print OUT qq{
BEGIN DATA;
DIMENSIONS NTAX=$n_sam NCHAR=$n_chs;
FORMAT DATATYPE=STANDARD MISSING=?;

MATRIX
};

for(my $i=0;$i<$n_sam;$i++){
	print OUT "$samples[$i][0]";
	for(my $n=0;$n<$n_chs;$n+=100){
		my $e = $n + 100;
		$e = $n_chs if($e > $n_chs);
		my $n_c = $e - $n;
		print OUT "\t", substr($data[$i], $n, $n_c), "\n";
	}
}

print OUT qq{;\nEND;\n};
print OUT qq{
BEGIN PAUP;
HSE ADDSEQ=RANDOM;
DESC 1 / PLOT=PHYLO;
SAVETR FILE= $opt_o.tre BRLENS=YES FOR=NEXUS;
SAVETR FILE= $opt_o.phylip.tre BRLENS=YES FOR=PHYLIP;
END;
};

close OUT;

1;

sub usage {
	print qq{Usage: $0 -n <freq_thresold:6> -s <complexity_thresold:200> -i <phylokmer_file> -o <nexus_file>\n};
	exit;
}

