import argparse
import os

from Utils import _readable_object


def setupParser():
	parser = argparse.ArgumentParser(description='Convert audio files to spectograms of given length')
	input_group = parser.add_argument_group(title="Input files",
											description="The audio files that should be converted "
														"to spectrograms. These can either be individual "
														"files or entire directories")
	input_group.add_argument('-i', '--input', action='append', type=_readable_object, required=True,
							 help='Audio file to be processed or directory containing audio files')

	parts_group = parser.add_mutually_exclusive_group()
	parts_group.add_argument('-s', '--seconds', action='store', type=int,
							 help='The length, in seconds, of the output files')
	parts_group.add_argument('-p', '--pieces', action='store', type=int,
							 help='The number of output files. '
								  'Their length will be evenly distributed, except for the last file which may '
								  'be shorter than the rest')
	parser.add_argument('-d', '--directory', action='store_false')
	return parser
