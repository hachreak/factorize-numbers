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
#print "u: ",$u," v: ",$v,"\n";
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

sub factorize_pollard_rho{
  # input data: number to factorize
  my $val = $_[0];

  if($val % 2 == 0){
    if($val != 2){
      # requires further decomposition
      factorize_pollard_rho($val / 2);
      print 2, " ";
      return 2;
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
=for
print "g: ",$g," val: ",$val," g is prime:";
if(is_prime($g)){
  print "si";
}else{
  print "no";
}
print "\n";
=cut
  if($g == $val){
     if(is_prime($g)){
       print $g," ";
     }else{
       factorize_pollard_rho($g);
     }
  }else{
     factorize_pollard_rho($g);
     factorize_pollard_rho($val / $g);
  }

  return $g;
}

sub factorize_brent{
  # input data: number to factorize
  my $val = $_[0];

  if($val % 2 == 0){
    if(2 == $val){
      print 2,"\n"
    }else{
      factorize_brent($val / 2);
    }
    return 2;
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
     }else{
       factorize_brent($g);
     }
  }else{
    factorize_brent($g);
    factorize_brent($val / $g);
  }
  return $g;
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
#my $val = 597659033765529481630;
#my $val = 779;
# Factorize number!
my $start_run = time();
my @fact = myfactorize($val);
my $end_run = time();
my $run_time = $end_run - $start_run;
print "Job took $run_time seconds\n";

$start_run = time();
my @fact2 = factorize_pollard_rho($val);
$end_run = time();
$run_time = $end_run - $start_run;
print "Job took $run_time seconds\n";

$start_run = time();
my @fact3 = factorize_brent($val);
$end_run = time();
$run_time = $end_run - $start_run;
print "Job took $run_time seconds\n";



print "\n";
# Print result in JSON..
print "[\"",join('","', @fact),"\"]";
