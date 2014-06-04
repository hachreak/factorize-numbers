#!/usr/bin/perl

use CGI;
use CGI::Carp qw(fatalsToBrowser);
use warnings;
use strict;

my $cgi = CGI->new;

# Here I'd like to receive data from jQuery via ajax.
my $id = 6;#$cgi->param('data_id');     
my $json = qq{{"ID" : "$id"}};

print $cgi->header('application/json');
print $json;
