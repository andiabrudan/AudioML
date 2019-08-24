from typing import List, Callable, Tuple

import numpy as np
from keras.utils import to_categorical
from Constants import SPEC_MAX_WIDTH, SPEC_MAX_HEIGHT
from Utils import *
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import tensorflow as tf

tf.compat.v1.enable_eager_execution()

isPicture: Callable[[str], bool] = lambda string: string.endswith(".png")


class FeatureFile:
	def __init__(self, path, label):
		self.path = path
		self.label = label

	def __str__(self):
		return f"{self.path} -> {self.label}"


class FeatureDirectory:
	def __init__(self, directory, genre):
		self.directory = directory
		self.genre = genre
		self.files: List[FeatureFile] = None

	def getAllFiles(self) -> List[FeatureFile]:
		if self.files is None:
			self.files = list()
			files = listDirectory(self.directory)
			for f in files:
				self.files.append(FeatureFile(f, self.genre))
		return self.files

	def __str__(self):
		return f"{self.directory}"


def readPNG(filepath, newsize: Tuple[int, int, int] = None):
	image = tf.io.read_file(filepath)
	image = tf.image.decode_png(image, channels=1)
	img_height, img_width, _ = image.shape
	if newsize is not None:
		image = tf.image.resize(image, newsize[:2])
		# image = tf.cast(image, tf.float32)
		# image /= 255.0
		image = tf.reshape(image, newsize)
	return image.numpy()


# Converts the spectrogram slices into a dataset file
def generateDataset(featurefiles: List[FeatureFile]):
	features = list()
	labels = list()

	# Gather all the data
	for ff in featurefiles:
		if not isPicture(ff.path):
			print(f"File {ff.path} is not a png. Skipping")
			continue
		features.append(readPNG(ff.path, (SPEC_MAX_WIDTH, SPEC_MAX_HEIGHT, 1)))
		labels.append(ff.label)

	# Encode the labels as integers
	encoder = LabelEncoder()
	encoder.fit(labels)
	labels = encoder.transform(labels)
	labels = to_categorical(labels)

	x_train, x_test, y_train, y_test = train_test_split(features, labels)
	x_train = np.array(x_train)
	x_test = np.array(x_test)
	# return the encoder so the data can be decoded
	return x_train, x_test, y_train, y_test, encoder


if __name__ == '__main__':
	x = readPNG("D:/free-spoken-digit-dataset-master/recordings/0_jackson_0/0_jackson_0_ch1_part1.png")
	y = 1
