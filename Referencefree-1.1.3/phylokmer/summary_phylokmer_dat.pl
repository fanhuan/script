#!/usr/bin/perl -w
#
#Author: Ruan Jue <ruanjue@gmail.com>
#
use Getopt::Std;

getopts("n:");

$opt_n |= 6;

my @samples = ();
my %clusters = ();

while(<>){
	if(/^#sample\d+:\s+(\S+)/){
		push(@samples, $1);
		next;
	} elsif(/^#/){
		next;
	}
	chomp;
	my @tabs = split;
	my $ind = '';
	for(my $i=2;$i<@tabs;$i++){
		$ind .= ($i - 2) . "\t" if($tabs[$i] >= $opt_n);
	}
	$clusters{$ind} ++ if(length($ind));
}

foreach my $key (sort keys %clusters){
	my $val = $clusters{$key};
	chomp $key;
	my @tabs = split /\s/, $key;
	my @sams = ();
	foreach my $ind (@tabs){
		push(@sams, $samples[$ind]);
	}
	print join(",", @sams), "\t$val\n";
}

1;
