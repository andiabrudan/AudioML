import argparse

from Utils import _readable_object


class act(argparse.Action):
	def __call__(self, parser, namespace, values, option_string=None):
		if not _readable_object(values[0]):
			raise argparse.ArgumentTypeError(f"Invalid value {values[0]}. This needs to be "
											 f"a readable file or directory")

		getattr(namespace, self.dest).append({"name": values[0],
											  "label": values[1]})


def tfparser():
	# parser = argparse.ArgumentParser(description="Train a model or use it to predict labels for some data")
	#
	# origin = parser.add_argument_group(title="How the model should be treated.",
	# 								   description="Whether an existing model should be loaded from disk, "
	# 											   "or a new one be created and if the model should be "
	# 											   "saved after processing or be discarded. The default "
	# 											   "is to instantiate a new model and discard it after "
	# 											   "use")
	#
	# origin.add_argument("-s", "--save", action="store",
	# 					help="If the model is to be saved. If you want it to overwrite an existing model, "
	# 						 "then do not specify any location. If this is a new model, then you need "
	# 						 "to specify a location on the disk")
	#
	# load = origin.add_mutually_exclusive_group()
	# disk = load.add_argument_group(title="If the model should be loaded from disk",
	# 							   description="In this case, the specified file should have the .tfmodel extension")
	# disk.add_argument("-l", "--load", action="store",
	# 				  help="The model that should be loaded. This has to be a valid .tfmodel file")
	#
	# load.add_argument("-n", "--new", action="store_true",
	# 				  help="If a new model should be created")
	#
	# input_group = parser.add_argument_group(title="Input files",
	# 										description="The files that should be used for training/predicting. "
	# 													"These can either be individual files or entire directories")
	# input_group.add_argument("-i", "--input", action='append', type=_readable_object, required=True,
	# 						 help="Files that should be processed. These can be audio files (of any extension) "
	# 							  "in which case they will first be converted to a spectrogram, or they can be "
	# 							  "images with extension .png in which case they will be used as is")
	#
	# train_predict = parser.add_mutually_exclusive_group(required=True)
	# train_predict.add_argument("-t", "--train", action="store_true",
	# 						   help="If the input files should be used for training")
	# train_predict.add_argument("-p", "--predict", action="store_true",
	# 						   help="If the input files should be predicted")
	#
	# parser.add_argument("-e", "--epochs", action="store", type=int, default=7,
	# 					help="The number of epochs the model should run for. "
	# 						 "Larger values are not necessarily better.")
	#
	# layers = parser.add_argument_group(title="The layers that make up the model",
	# 								   description="")

	### Main Parser
	parser = argparse.ArgumentParser(description="Train a model or use it to predict labels for some data")
	origin = parser.add_argument_group(title="How the model should be treated.",
									   description="Whether an existing model should be loaded from disk, "
												   "or a new one be created and if the model should be "
												   "saved after processing or be discarded. The default "
												   "is to instantiate a new model and discard it after "
												   "use")
	origin.add_argument("-s", "--save", action="store", nargs='?',
						help="If the model is to be saved. If you want it to overwrite an existing model, "
							 "then do not specify any location. If this is a new model, then you need "
							 "to specify a location on the disk")
	load = origin.add_mutually_exclusive_group()
	load.add_argument("-l", "--load", action="store", nargs=1,
					  help="If the model should be loaded from disk. "
						   "In this case, the specified file should be a valid .tfmodel file")

	load.add_argument("-n", "--new", action="store_true",
					  help="If a new model should be created")
	### End Main Parser

	subparsers = parser.add_subparsers(title="Action", required=True,
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
	return parser


if __name__ == '__main__':
	parser = tfparser()
	args = parser.parse_args()
	print(args)
