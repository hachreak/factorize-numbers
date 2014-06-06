#!/usr/bin/perl

use CGI;
use warnings;
use strict;
use bigint;
use List::Util qw[min max];

##
# Compute gcd (greatest common divisor)
sub gcd($$) {
  my ($u, $v) = @_;
  while ($v) {
    ($u, $v) = ($v, $u % $v);
  }
  return abs($u);
}

##
# Test if is a prime number
##
sub is_prime($){
  my ($num) = @_;
  for(my $i=2; $i<int(sqrt($num)+1); $i++){
    if($num % $i == 0){
      return 0; # false
    }
  }
  return 1; # true
}

###
# Factorize a integer number.
#
# @param val number to factorize
# @return array of prime numbers
##
sub myfactorize{
  # input data: number to factorize
  my $val = $_[0];
  # output data: array of prime numbers
  my @fact = ();
  
  # Even numbers: look if the number is divisible for 2
  while ($val%2 == 0) {
    push(@fact, 2);
    $val = $val/2;
  }
 
  # Odd numbers:
  for (my $i = 3; $i <= (int(sqrt($val))+1); $i = $i+2) {
    # While i divides n
    while ($val % $i == 0){
      push(@fact, $i);
      $val = $val / $i;
    }
  }
 
  # If the number is a prime number greater than 2
  if ($val > 2){
    push(@fact, $val);
  }

  return @fact;
}

sub factorize_pollard_rho{
  # input data: number to factorize
  my($val, @fact) = @_;

  if($val % 2 == 0){
    if($val != 2){
      # requires further decomposition
      @fact = factorize_pollard_rho($val / 2, @fact);
      print 2, " ";
      push(@fact, 2);
      return @fact;
    }
  }

  # random number in range [1, $val - 1]
  my $x = int(rand($val - 1)) + 1;
  my $y = $x;
  my $c = int(rand($val - 1)) + 1;
  my $g = 1;
 
  while($g == 1){
    $x = (($x * $x) % $val + $c) % $val;
    $y = (($y * $y) % $val + $c) % $val;
    $y = (($y * $y) % $val + $c) % $val;
    $g = gcd(abs($x - $y), $val);
  }

  if($g == $val){
     if(is_prime($g)){
       print $g," ";
       push(@fact, $g);
     }else{
       @fact = factorize_pollard_rho($g, @fact);
     }
  }else{
     @fact = factorize_pollard_rho($g, @fact);
     @fact = factorize_pollard_rho($val / $g, @fact);
  }

  return @fact;
}

sub factorize_brent{
  # input data: number to factorize
  my($val, @fact) = @_;

  if($val % 2 == 0){
    if(2 != $val){
      @fact = factorize_brent($val / 2, @fact);
    }
    print 2,"\n";
    push(@fact, 2);
    return @fact;
  } 

  # random number in range [1, $val - 1]
  my $y = int(rand($val - 1)) + 1;
  my $c = int(rand($val - 1)) + 1;
  my $m = int(rand($val - 1)) + 1;

  # init vars
  my $g = 1;
  my $r = 1;
  my $q = 1;
  my $ys = 1;
  my $x = 1;

  while($g == 1){
    my $x = $y;
    my $k = 0;

    for(my $i=0; $i<$r; $i++){
      $y = (($y * $y) % $val + $c) % $val;
    }

    while($k < $r && $g == 1){
      $ys = $y;
      
      for(my $i=0; $i<min($m, $r - $k); $i++){
        $y = (($y * $y) % $val + $c) % $val;
        $q = $q * (abs($x - $y)) % $val;
      }

      $g = gcd($q, $val);
      $k = $k + $m;
    }

    $r = $r * 2;
  }

  if($g == $val){
    while($g == 1){
      $ys = (($ys * $ys) % $val + $c) % $val;
      $g = gcd(abs($x - $ys), $val);
    }
  }

  if($g == $val){
     if(is_prime($g)){
       print $g," ";
       push(@fact, $g);
     }else{
       @fact = factorize_brent($g, @fact);
     }
  }else{
    @fact = factorize_brent($g, @fact);
    @fact = factorize_brent($val / $g, @fact);
  }
  return @fact;
}

=for
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
=cut

my $val = 59765903376552948163;
#my $val = 40;
#my $val = 779;
# Factorize number!
my @fact = myfactorize($val);
#my @fact = factorize_pollard_rho($val);
#my @fact = factorize_brent($val);

print "\n";
# Print result in JSON..
print "[\"",join('","', @fact),"\"]";
print "\n";
