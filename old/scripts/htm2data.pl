#!/usr/bin/env perl

use utf8;
use File::Basename;
use Encode;

# table numeral
# numeral trans chan_name variant comment

# table general comment
# chan_name comment variant
$sups="";
$wdir = "/Users/bibiko/Documents/MPI/Colleagues/Numerals/htm";

$outfilecom  = "/Users/bibiko/Documents/MPI/Colleagues/Numerals/comment_new.tab";
$outfiledata = "/Users/bibiko/Documents/MPI/Colleagues/Numerals/data_gt2.tab";

opendir $dir, $wdir or die "Cannot open directory: $!";
@files = readdir $dir;
closedir $dir;

open(COM, '>:encoding(UTF-8)', $outfilecom) or die "Could not open file '$outfilecom' $!";
open(DAT, '>:encoding(UTF-8)', $outfiledata) or die "Could not open file '$outfiledata' $!";


foreach $fh (@files) {

	next if ($fh !~ m/\.htm$/);

	$f = "$wdir/$fh";
	print "$f\n";

	$chan_name = basename($f);
	$table_counter = 0;
	@gen_com = ();

	open(HTM, '<:encoding(UTF-8)', $f) or die "Could not open file '$f' $!";
	while($line = <HTM>) {

		chomp($line);

		$table_counter++ if($line =~ m/<table/);

		# if ($table_counter == 2 or $table_counter == 6) {
		if (($table_counter+2)%4 == 0) {
			if($line =~ m/>(\d+)\.?\s*(.+)$/) {
				$num = $1;
				$trans = $2;
				$var = ($table_counter+2)/4; #($table_counter == 2) ? 1 : 2;
				$com = "";

				$trans =~ s/<span[^>]*?>//g;
				$trans =~ s/<p[^>]*?>//g;
				$trans =~ s/<\/p>//g;
				$trans =~ s/<\/span>//g;
				$trans =~ s/<\/[bi]>//g;
				$trans =~ s/<[bi]>//g;

				$trans =~ s/\s+/ /g;

				$trans =~ s/<sup>(.*?)<\/sup>/convertSup($1)/ge;
				$trans =~ s/<[^>]*?>//g;

				$trans =~ s/&lt;/</g;
				$trans =~ s/&gt;/>/g;
				$trans =~ s/&amp;/&/g;
				$trans =~ s/\s+([\}\]\)])/$1/g;
				$trans =~ s/([\{\[\(])\s+/$1/g;
				$trans =~ s/^\s+//;

				$trans =~ s/^([^\(<\{]*?)\//$1#/g;
				$trans =~ s/^([^\(<\{]*?)\//$1#/g;
				$trans =~ s/^([^\(<\{]*?)\//$1#/g;
				$trans =~ s/^([^\(<\{]*?)\//$1#/g;
				$trans =~ s/^([^\(<\{]*?)\//$1#/g;
				# $trans =~ s/^([^\(<\{]*?)\[/$1#/g;
				# $trans =~ s/^([^\(<\{]*?)\[/$1#/g;
				# $trans =~ s/^([^\(<\{]*?)\[/$1#/g;
				# $trans =~ s/^([^\(<\{]*?)\[/$1#/g;
				# $trans =~ s/^([^\(<\{]*?)\[/$1#/g;
				$trans =~ s/^([^\(<\{]*?)[,;]/$1#/g;
				$trans =~ s/^([^\(<\{]*?)[,;]/$1#/g;
				$trans =~ s/^([^\(<\{]*?)[,;]/$1#/g;
				$trans =~ s/^([^\(<\{]*?)[,;]/$1#/g;
				$trans =~ s/^([^\(<\{]*?)[,;]/$1#/g;

				$trans =~ s/^(\S+?\(\S+\)),/$1#/g;
				$trans =~ s/^(\S+?\(\S+\)),/$1#/g;

				@tr = split(/\s*#\s*/, $trans);
				foreach $tra (@tr) {
					$trans1 = $tra;
					# $trans1 =~ s/\]//g;
					if($tra =~ m/[\s\(][<\(\{]/) {
						$tra =~ m/^(.*?)\s+([<\(\{].*?[\}\)]?)$/;
						$trans1 = $1;
						$com = $2;
					} elsif($tra =~ m/\s+\[\s*\(/) {
						$tra =~ m/^(.*?)\s+(\[\s*\(.*?\])$/;
						$trans1 = $1;
						$com = $2;
					}
					# $trans1 =~ s/\]//g;
					if($trans1 =~ m/[*＊]/) {
						$trans1 =~ s/([*＊]+)//g;
						$ln = $1;
						$ln = length($ln);
						$com .= " ";
						for ($i = 0; $i < $ln; $i++) {
							$com .= "*";
						}
					}
					$trans1 =~ s/^\s+//;
					$trans1 =~ s/\s$//;
					$trans1 =~ s/^\?+$//;
					$com =~ s/^\s+//;
					$com =~ s/\s$//;
				
					if($var>2 and length($trans1) > 0) {
						print DAT "$num\t$trans1\t$chan_name\t$var\t$com\n";
					}
				}

			}

		}


		# if ($table_counter == 4 or $table_counter == 8) {
		if ($table_counter%4 == 0) {
			# $cvar = ($table_counter == 4) ? 0 : 1;
			$cvar = ($table_counter+2)/4 - 1;
			$gen_com[$cvar] .= $line . "\n";
		}

	}

	close HTM;

	$cnt=1;
	foreach $c (@gen_com) {
		$cm = $c;
		$cm =~ s/<[^>]+?>//g;
		$cm =~ s/&lt;/</g;
		$cm =~ s/&gt;/>/g;
		$cm =~ s/&amp;/&/g;
		$cm =~ s/^[\s\n]*//smg;
		$cm =~ s/[\s\n]*$//smg;
		$cm =~ s/other\s+comments\s*:?\s*//i;
		$cm =~ s/\n/\\n/g;
		$cm =~ s/\\nBack >>.*$//sm;
		$cm =~ s/Back >>.*$//sm;
		$cm =~ s/^\s+//;
		$cm =~ s/\s$//;
		print COM "$chan_name\t$cm\t$cnt\n" if(length($cm) > 0);
		$cnt++;
	}

}

close COM;
close DAT;
print "----";
print $sups;

sub convertSup {
	$x = shift;
	$sups.=$x;
	$x =~ s/1/¹/g;
	$x =~ s/2/²/g;
	$x =~ s/3/³/g;
	$x =~ s/4/⁴/g;
	$x =~ s/5/⁵/g;
	$x =~ s/6/⁶/g;
	$x =~ s/7/⁷/g;
	$x =~ s/8/⁸/g;
	$x =~ s/9/⁹/g;
	$x =~ s/0/⁰/g;
	$x =~ s/h/ʰ/g;
	$x =~ s/j/ʲ/g;
	$x =~ s/y/ʸ/g;
	$x =~ s/ / /g;
	$x =~ s/ / /g;
	$x =~ s/ʔ/ˀ/g;
	$x =~ s/Ɂ/ˀ/g;
	$x =~ s/u/ᵘ/g;
	$x =~ s/i/ⁱ/g;
	$x =~ s/ʁ/ʶ/g;
	$x =~ s/w/ʷ/g;
	$x =~ s/L/ᴸ/g;
	$x =~ s/H/ᴴ/g;
	$x =~ s/e/ᵉ/g;
	$x =~ s/a/ᵃ/g;
	$x =~ s/g/ᵍ/g;
	$x =~ s/ʀ/ᴿ/g;
	$x =~ s/ʌ/ᶺ/g;
	$x =~ s/ʊ/ᶷ/g;
	$x =~ s/\(/⁽/g;
	$x =~ s/\)/⁾/g;
	$x =~ s/ə/ᵊ/g;
	$x =~ s/-/⁻/g;
	$x =~ s/ɪ/ᶦ/g;
	$x =~ s/ø/%%ø/g;
	$x =~ s/ɾ/%%ɾ/g;
	return($x);
}