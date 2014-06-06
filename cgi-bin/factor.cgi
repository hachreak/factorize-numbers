#!/usr/bin/perl

use CGI;
use warnings;
use strict;
use bigint;

###
# Factorize a integer number.
#
# @param val number to factorize
# @return array of prime numbers
##
sub factorize{
  # input data: number to factorize
  my $val = $_[0];
  # output data: array of prime numbers
  my @fact = ();
  
  # Uncomment to remove duplicate
  # my $last = 0;

  # Even numbers: look if the number is divisible for 2
  while ($val%2 == 0) {
  # Uncomment next 3 lines to remove duplicate
  # if($last != 2){
      push(@fact, 2);
  # }
    $val = $val/2;
  # $last = 2;
  }
 
  # Odd numbers:
  for (my $i = 3; $i <= (int(sqrt($val))+1); $i = $i+2) {
    # While i divides n
    while ($val % $i == 0){
    # Uncomment next 3 lines to remove duplicate
    # if($last != $i){
        push(@fact, $i);
    # }
      $val = $val / $i;
    # $last = $i;
    }
  }
 
  # If the number is a prime number greater than 2
  if ($val > 2){
    push(@fact, $val);
  }

  return @fact;
}

# CGI 
my $q = CGI->new;

# Process an HTTP request
my $val = $q->param('number');

# Check input data, unless return a error!
unless ($val =~ /^\d+$/){
 print $q->header('application/json','422 Invalid input data!');
 exit;
}

# Prepare various HTTP responses
print $q->header('application/json');

#my $start_run = time();
# Factorize number!
my @fact = factorize($val);
#my $end_run = time();
#my $run_time = $end_run - $start_run;
#print "Job took $run_time seconds\n";

# Print result in JSON..
print "[\"",join('","', @fact),"\"]";
