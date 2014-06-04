#!/usr/bin/perl
use warnings;
use strict;
use bigint;

my $x = 2 + 4.5;
print $x,"\n";	# BigInt 6
print 2 ** 512,"\n";	# really is what you think it is
print inf + 42,"\n";	# inf
print NaN * 7,"\n";	# NaN
print hex("0x1234567890123490"),"\n";	# Perl v5.10.0 or later
{
	no bigint;
	print "no bigint\n";
	print 2 ** 256,"\n";	# a normal Perl scalar now
}
print "ok bigint\n";
# Import into current package:
use bigint qw/hex oct/;
print hex("0x1234567890123490"),"\n";
print oct("01234567890123490"),"\n";
