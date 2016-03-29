#!/usr/bin/perl -w
#
#Author: Ruan Jue <ruanjue@gmail.com>
#
use strict;

while(<>){
	my ($kmer, $kcnt, $seqs) = split;
	my @rds = ();
	my %hash = ();
	while($seqs=~/(\d+):([ACGTNacgtn.]+):(\d+)/g){
		next if(exists $hash{$1});
		push(@rds, [$1, $2, $3]);
		$hash{$1} = 1;
	}
	@rds = sort {$a->[0] <=> $b->[0]} @rds;
	$kcnt = @rds;
	print "#$kmer\t$kcnt\n";
	print join("", map {">$_->[0] $_->[2]\n$_->[1]\n"} @rds);
}

1;
