import argparse

from Utils import _readable_object, _readable_directory, _readable_file


class act(argparse.Action):
	def __call__(self, parser, namespace, values, option_string=None):
		if not _readable_object(values[0]):
			raise argparse.ArgumentTypeError(f"Invalid value {values[0]}. This needs to be "
											 f"a readable file or directory")

		getattr(namespace, self.dest).append({"name": values[0],
											  "label": values[1]})


def tfparser():
	### Main Parser
	parser = argparse.ArgumentParser(description="Train a model or use it to predict labels for some data")
	origin = parser.add_argument_group(title="How the model should be treated.",
									   description="Whether an existing model should be loaded from disk, "
												   "or a new one be created and if the model should be "
												   "saved after processing or be discarded. The default "
												   "is to instantiate a new model and discard it after "
												   "use")
	origin.add_argument("-s", "--save", action="store", type=_readable_directory,
						help="If the model is to be saved. If you want it to overwrite an existing model, "
							 "then do not specify any location. If this is a new model, then you need "
							 "to specify a location on the disk")
	origin.add_argument("-l", "--load", action="store", type=_readable_directory,
						help="The location of the model you wish to use. "
							 "This location should be a directory containing a .json file "
							 "(with the model architecture) and an .hdf5 file (with the "
							 "weights for the model)")
	### End Main Parser

	subparsers = parser.add_subparsers(title="Action", required=True, dest="command",
									   description="What action should be performed")

	### Training subparser
	train = subparsers.add_parser("train", help="Train a new model or further reinforce an existing model")
	train.add_argument("-i", "--input", action=act, default=list(),
					   required=True, nargs=2, metavar=("INPUT", "LABEL"),
					   help="Files that should be processed. These can be audio files (of any extension) "
							"in which case they will first be converted to a spectrogram, or they can be "
							"images with extension .png in which case they will be used as is. The label "
							"will be used train the model")

	train.add_argument("-e", "--epochs", action="store", type=int, default=7,
					   help="The number of epochs the model should run for. "
							"Larger values are not necessarily better.")
	### End Training subparser

	### Predicting subparser
	predict = subparsers.add_parser("predict", help="Predict the label of one or more files using "
													"an existing, already trained model")

	predict.add_argument("-i", "--input", action="append", type=_readable_object, required=True,
						 help="The input files you want to predict. "
							  "They can be individual files or entire directories")

	### End Predicting subparser
	return parser


if __name__ == '__main__':
	parser = tfparser()
	args = parser.parse_args()
	print(args)
