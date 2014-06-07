#!/usr/bin/perl

use CGI;
use warnings;
use strict;
use bigint;
use List::Util qw[min max];

# my lib
use factor_lib qw(gcd is_prime myfactorize factorize_pollard_rho factorize_brent);

#############################

# CGI 
my $q = CGI->new;

# Process an HTTP request
my $val = $q->param('number');
my $algorithm = $q->param('algorithm');

# Securely check input data, unless return a error!
unless ($val =~ /^\d+$/ && $algorithm =~ /^[a-zA-Z0-9]+$/){
 print $q->header('application/json','422 Invalid input data!');
 exit;
}

# init randomizer
srand(time() | $$);

# Factorize number!
my @fact = ();
if($algorithm eq 'myfactorize'){
  @fact = myfactorize($val);
}else{
  if($algorithm eq 'pollardrho'){
    @fact = factorize_pollard_rho($val);
  }else{
    if($algorithm eq 'brent'){
      @fact = factorize_brent($val);
    }else{ 
      print $q->header('application/json','422 Invalid algorithm!');
      exit;
    }
  }
}

# Prepare various HTTP responses
print $q->header('application/json');

# Print result in JSON..
print "[\"",join('","', @fact),"\"]";
