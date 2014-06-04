#!/usr/bin/perl -w
use warnings;
use strict;

my $val = 38695000000000000000;
my $divisor = 2;
my @fact = ();

while($val > 1){
#  print "test ",$val," % ",$divisor,"\n";
  if($val % $divisor == 0){
    push(@fact, $divisor);
    $val /= $divisor;
  }else{
    $divisor++;
  }
}

foreach $val (@fact) {
 print $val," ";
}
print "\n";
