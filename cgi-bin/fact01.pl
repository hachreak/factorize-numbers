#!/usr/bin/perl
use warnings;
use strict;

#my $val = 38695000000000000000000;
my $val = 9963651140513278845267767820429449130664470383;
my $divisor = 2;
my @fact = ();

while($val > 1 or $val % 2 == 0){
  push(@fact, $divisor);
  $val /= 2;
}

$divisor++;

while($val > 1){
#  print "test ",$val," % ",$divisor,"\n";
  if($val % $divisor == 0){
    push(@fact, $divisor);
    $val /= $divisor;
  }else{
    $divisor += 2;
  }
}

foreach $val (@fact) {
 print $val," ";
}
print "\n";
