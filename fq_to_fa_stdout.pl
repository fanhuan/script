#!/usr/bin/perl
$|=1;
$in=shift;
#$out=shift;
open IN,"<$in";
open OUT,">$out";
while($line=<IN>){
     chomp $line;
     if ($line=~/^@/) {$i=0;$line=~s/@//; $id=$line;}
     $i++;
     if ($i==2 ){
      print ">$id\n$line\n";next;}
       
                   }
