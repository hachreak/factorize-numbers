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

use factor_lib qw(gcd is_prime myfactorize factorize_pollard_rho factorize_brent);

my $MAX = 10000000000;
my $CICLES = 20;

#############################

sub test_factor_lib{
  my($MAX, $CICLES, $IS_RAND, $DEBUG) = @_;
  my $val = 0;

  for(my $i=0; $i<$CICLES; $i++){
    if($IS_RAND){
      $val = int(rand($MAX - 1)) + 1;
    }else{
      $val = $i;
    }

    if($DEBUG){
      print "Number ",$i," [",$val,"]\n";
    }

    # Factorize number!
    my @fact1 = myfactorize($val);
    my @fact2 = sort {$a <=> $b} factorize_pollard_rho($val);
    my @fact3 = sort {$a <=> $b} factorize_brent($val);

    if($DEBUG){
      print "Factorize 1: ", join(", ", @fact1)."\n";
      print "Pollard-Rho: ", join(", ", @fact2)."\n";
      print "Brent:       ",join(", ", @fact3)."\n";
    }

    my $total1 = 1;
    my $total2 = 1;
    my $total3 = 1;
    my $v = 1;

    foreach $v (@fact1){
      $total1 *= $v;
    }
    foreach $v (@fact2){
      $total2 *= $v;
    }
    foreach $v (@fact3){
      $total3 *= $v;
    }

    if(scalar @fact1 != scalar @fact2 || scalar @fact2 != scalar @fact3){
      print "[ASSERT ERROR] number of elements found is different!\n";
    }

    for(my $i=0; $i<scalar @fact1; $i++){
      if($fact1[$i] != $fact2[$i] || $fact2[$i] != $fact3[$i]){
        print "[ASSERT ERROR] some elements found is different!\n";
      }
    }

    if($total1 != $total2 || $total2 != $total3 || $total3 != $val){
      print "[ASSERT ERROR] the multiplication is different\n";
    }  
  }
}

# init randomizer
srand(time() | $$);

test_factor_lib($MAX, $CICLES, 0, 1);
test_factor_lib($MAX, $CICLES, 1, 1);

#print join(", ", factorize_pollard_rho(99));
