#!/usr/bin/perl -w
use warnings;
use strict;

my @mylist  = (124,567,899)[1,2];
my @mylist2 = (124,567,899)[1..2];

print "val: ",$mylist[1],"\n";
print "val: ",$mylist2[1],"\n";

