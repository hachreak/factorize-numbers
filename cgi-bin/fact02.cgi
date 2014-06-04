#!/usr/bin/perl
use CGI;
use warnings;
use strict;
use bigint;

my $q = CGI->new;
#my @fact = ();

sub factorize{
  my @fact = ();
  my $val = $_[0];
  my $last = 0;

  # Even numbers: look if the number is divisible for 2
  while ($val%2 == 0) {
#    if($last != 2){
      push(@fact, 2);
#    }
    $val = $val/2;
    $last = 2;
  }
 
  # Odd numbers:
  for (my $i = 3; $i <= (int(sqrt($val))+1); $i = $i+2) {
    # While i divides n
    while ($val % $i == 0){
#      if($last != $i){
        push(@fact, $i);
#      }
      $val = $val / $i;
      $last = $i;
    }
  }
 
  # If the number is a prime number greater than 2
  if ($val > 2){
    push(@fact, $val);
  }

  return @fact;
}

#print $q->header('type application/json','401 Authorization Required!');
#exit;
# Process an HTTP request
my $val = $q->param('number');
my $callback = $q->param('callback');
#my $backup = $val;

unless ($val =~ /^[+-]?\d+$/){
 print $q->header('type application/json','422 Invalid input data!');
 exit;
}

# Prepare various HTTP responses
print $q->header('application/json');

my $start = time;
my @fact = factorize($val);
my $duration = time - $start;
#print "Execution time: $duration s\n";

print $callback,"([",join(',', @fact),"])";
