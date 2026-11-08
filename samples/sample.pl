# Sample Perl code to test Bluloco Dark
# Includes regex and hash maps

use strict;
use warnings;

my %theme_colors = (
    bg => '282C34',
    fg => 'ABB2BF',
);

my $text = "Welcome to Bluloco Dark Theme";
if ($text =~ /Bluloco/) {
    print "Found theme name in text\n";
}

foreach my $key (keys %theme_colors) {
    print "$key: $theme_colors{$key}\n";
}
