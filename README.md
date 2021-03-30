# Burrows-Wheeler-Transform
Aim: Implementation of Burrows-Wheeler Transformation (BWT) and
Ferragina-Manzini (FM) index. The implementation haves two parts:
	- Given a long text from the DNA alphabet it will generate and save
	the BWT string, the FM-index, and the suffix array. The input file 
	format will be FASTA. There will be two output index files. First, 
	it will generate a file with extension ".bwt", which will be a text 
	file that contains the BWT string. The second file with extension ".fm"
	will include the FM-index tables and the suffix array. 
	- Given the BWT file (.bwt) and a pattern to search in FASTA format, 
	find all exact match locations of the pattern in the text.

# bwtf.py

bwtf is a program that performs Burrows-Wheeler transformation with 
1. indexing,
2. searching and 
3. inverse transform operations.

## Installation

bwtf uses Python 3 standard libraries.
If you have installed Python 3 before, no additional package is needed.
If not, you may install Python 3 from "https://www.python.org/downloads/".
Make sure you have selected the appropriate distribution for your operating system.

## Usage

You can run the program using terminal.

The syntax:

"python bwtf.py 'mode' 'text.fa' --pattern(optional) 'pattern.fa(optional)'"

'mode'			: Mode selection
					Appropriate selections are:
					- '--index' for indexing
					- '--search' for searching
					- '--inverse' for inverse bw transformation

'text.fa' 		: File in the FASTA format, containing the text T in which the pattern will be searched
--pattern		: (Optional)Indicator that the next input is the pattern file sor '--search' mode
'pattern.fa'	: File in the FASTA format, containing the pattern P to be searched in T

## Examples:

1. Indexing:
Input >>> python bwtf.py --index "hw2example.fa"

Output >>>
Indexing has been done. -> hw2example.fa.bwt , hw2example.fa.fm

2. Searching:
Input >>> python bwtfm.py --search "hw2example.fa" --pattern "hw2pattern.fa"

Output >>>
Pattern P found in T  2 times at positions:
Pos  1 :  5
Pos  2 :  2
Search completed in 0.00 seconds.

3. Inverse Transform:
Input >>> python bwtfm.py --inverse "hw2example.fa"

Output >>>
The data has been recovered. -> hw2example.fa.ibwt
