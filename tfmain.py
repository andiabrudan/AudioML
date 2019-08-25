from typing import List, Dict
import numpy as np
import tensorflow as tf
from Constants import SPEC_MAX_WIDTH, SPEC_MAX_HEIGHT, SPEC_NUM_CHANNELS
from MyModel import MyModel
from Utils import isDirectory, listDirectory, isFile, listAllSubDirectories, buildDirPath
from tfparser import tfparser
from Dataset import FeatureDirectory, generateDataset, FeatureFile, readImage
import os

config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth = True
# config.gpu_options.per_process_gpu_memory_fraction = 0.8
tf.compat.v1.enable_eager_execution(config=config)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


def gatherFiles(locations: List[Dict[str, str]]) -> List[FeatureFile]:
	feature_files: List[FeatureFile] = list()

	# Special case if only 1 single directory was provided which contains other directories
	special = locations[0]["name"]
	if len(locations) == 1 and isDirectory(special):
		subdirectories = listAllSubDirectories(special)
		for subdir in subdirectories:
			feature_directory = FeatureDirectory(directory=buildDirPath(special, subdir),
												 label=subdir)
			files = feature_directory.getAllFiles()
			feature_files += files
		return feature_files

	for item in locations:
		if isDirectory(item["name"]):
			files = FeatureDirectory(item["name"], item["label"]).getAllFiles()
			feature_files += files
		else:
			feature_files.append(FeatureFile(item["name"], item["label"]))
	return feature_files


def doTraining(locations: List[Dict[str, str]], model: MyModel, create_new: bool):
	print("Gathering files... ", end='')
	feature_files: List[FeatureFile] = gatherFiles(locations)
	print("Done")

	print("Generating dataset... ", end='')
	x_train, x_test, y_train, y_test, encoder = generateDataset(feature_files)
	print("Done")

	if create_new:
		print(f"No model was loaded, creating a new one... ", end='')
		model.createNew(len(encoder.classes_))
		print("Done")

	model.setEncoder(encoder)
	model.getinstance().summary()
	model.getinstance().fit(x_train,
							y_train,
							epochs=epochs,
							batch_size=32,
							verbose=1)
	loss, accuracy = model.getinstance().evaluate(x_test, y_test)
	print(f"Accuracy: {accuracy * 100:.5f}")

	if model.savingEnabled():
		savelocation = model.getSaveDirectory()
		print(f"Saving model to: \"{savelocation}\"... ", end='')
		model.saveModelArchitecture()
		model.saveModelWeights()
		model.saveEncoder()
		print("Done")


def doPredicting(locations: List[str], model: MyModel):
	if model is None:
		print("Cannot predict on a new model. "
			  "Train a model first and save it, then load it for prediction.")
		return

	# Gather all files
	print("Gathering files... ", end='')
	files = list()
	for item in locations:
		if isFile(item):
			files.append(item)
		elif isDirectory(item):
			files += listDirectory(item)
	print("Done")

	# Read the files and convert them all into
	# a numpy array of matrices (each matrix being a picture)
	pics = list()
	for f in files:
		pics.append(readImage(f, (SPEC_MAX_WIDTH, SPEC_MAX_HEIGHT, SPEC_NUM_CHANNELS)))
	pics = np.array(pics)

	print("Predicting... ", end='')
	# Do the prediction
	predictions = model.getinstance().predict(pics)
	predictions = model.decode(predictions)
	print("Done\n")

	# Print the predictions
	for i in range(len(files)):
		print(f"File \"{files[i]}\" was predicted to be: {predictions[i]}")


if __name__ == '__main__':
	args = tfparser().parse_args()
	# extract command line arguments
	save = args.save
	load = args.load
	command = args.command

	# initialize values that we work with
	model = MyModel()
	create_new = True

	if save:
		print(f"Save location has been set to {save}")
		model.setSaveDirectory(save)

	if load:
		print(f"Loading model from {load}... ", end='')
		model.loadModelArchitecture(load)
		model.loadModelWeights(load)
		model.loadEncoder(load)
		print("Done")
		create_new = False
	else:
		create_new = True

	if command == "train":
		epochs = args.epochs
		print("Beginning to train model")
		doTraining(args.input, model, create_new)

	elif command == "predict":
		print("Beginning to predict model")
		doPredicting(args.input, model)

	else:
		print(f"Unknown command \"{command}\"")
