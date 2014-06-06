#!/usr/bin/perl

package factor_lib;

use warnings;
use strict;
use bigint;
use List::Util qw[min max];

use Exporter qw(import);
 
our @EXPORT_OK = qw(gcd is_prime myfactorize factorize_pollard_rho factorize_brent);

##
# Compute gcd (greatest common divisor)
#
# @param @u first number
# @param @v second number
# @return greatest common divisor
#
sub gcd($$) {
  my ($u, $v) = @_;
  while ($v) {
    ($u, $v) = ($v, $u % $v);
  }
  return abs($u);
}

##
# Test if is a prime number
#
# @param $num number to test
# @return true if it's a prime number
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
# 1° Algorithm: Factorize a integer number.
#
# @param $val number to factorize
# @return array of prime numbers
##
sub myfactorize{
  # input data: number to factorize
  my $val = $_[0];
  # output data: array of prime numbers
  my @fact = ();
  
  # if zero or 1, return!
  if($val == 0 || $val == 1){
    return $val;
  }

  # Even numbers: look if the number is divisible for 2
  while ($val%2 == 0) {
    push(@fact, 2);
    $val = $val/2;
  }
 
  # Odd numbers:
  for (my $i = 3; $i <= (int(sqrt($val))+1); $i = $i+2) {
    # While i divides n
    while ($val % $i == 0){
      push(@fact, int($i));
      $val = $val / $i;
    }
  }
 
  # If the number is a prime number greater than 2
  if ($val > 2){
    push(@fact, int($val));
  }

  return @fact;
}

###
# 2° Algorithm: Factorize a integer number using Pollard-Rho algorithm.
#
# @param $val number to factorize
# @param @fact array of already found divisors
# @return array of prime numbers
##
sub factorize_pollard_rho{
  # input data: number to factorize
  my($val, @fact) = @_;

  # if $val is equal to 1 or 0, don't continues
  if($val == 1 || $val == 0){
    push(@fact, $val);
    return @fact;
  }

  # test if even number
  if($val % 2 == 0){
    if($val != 2){
      # requires further decomposition
      @fact = factorize_pollard_rho($val / 2, @fact);
      push(@fact, 2);
      return @fact;
    }
  }

  # random number in range [1, $val - 1] and init vars
  my $x = int(rand($val - 1)) + 1;
  my $y = $x;
  my $c = int(rand($val - 1)) + 1;
  my $g = 1;
 
  # try to decompose
  while($g == 1){
    $x = (($x * $x) % $val + $c) % $val;
    $y = (($y * $y) % $val + $c) % $val;
    $y = (($y * $y) % $val + $c) % $val;
    $g = gcd(abs($x - $y), $val);
  }

  # looks the result
  if($g == $val){
     # try to see if it's a "semiprime"
     if(is_prime($g)){
       # it's a prime number, finish! push the result in array
       push(@fact, int($g));
     }else{
       # try to decompose in prime numbers
       @fact = factorize_pollard_rho($g, @fact);
     }
  }else{
     # found n*q=val, continues to decompose in prime numbers
     @fact = factorize_pollard_rho($g, @fact);
     @fact = factorize_pollard_rho($val / $g, @fact);
  }

  # return the list of prime numbers found
  return @fact;
}

###
# 3° Algorithm: Factorize a integer number using Brent algorithm (Pollard-Rho optimization).
#
# @param $val number to factorize
# @param @fact array of already found divisors
# @return array of prime numbers
##
sub factorize_brent{
  # input data: number to factorize
  my($val, @fact) = @_;

  # if $val is equal to 1 or 0, don't continues
  if($val == 1 || $val == 0){
    push(@fact, $val);
    return @fact;
  }

  # test if it's a even number
  if($val % 2 == 0){
    if(2 != $val){
      @fact = factorize_brent($val / 2, @fact);
    }
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

  # try to decompose
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

  # looks the result
  if($g == $val){
     # try to see if it's a "semiprime"
     if(is_prime($g)){
       # it's a prime number, finish! push the result in array
       push(@fact, $g);
     }else{
       # try to decompose in prime numbers
       @fact = factorize_brent($g, @fact);
     }
  }else{
    # found n*q=val, continues to decompose in prime numbers
    @fact = factorize_brent($g, @fact);
    @fact = factorize_brent($val / $g, @fact);
  }

  return @fact;
}

