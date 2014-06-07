=for
/**
 * Copyright (C) 2014 Leonardo Rossi <leonardo.rossi@studenti.unipr.it>
 *
 * This source code is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This source code is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this source code; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
 *
 */
=cut

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
