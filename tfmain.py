from typing import List
import tensorflow as tf
from tensorflow.python.keras.layers \
	import Dense, Flatten, Activation, \
	Conv2D, Dropout, BatchNormalization, MaxPooling2D
from Utils import isDirectory
from tfparser import tfparser
from Constants import SPEC_MAX_WIDTH, SPEC_MAX_HEIGHT
from Dataset import FeatureDirectory, generateDataset, FeatureFile
import os

os.environ['CUDA_VISIBLE_DEVICES'] = "0"
tf.compat.v1.enable_eager_execution()
# tf.keras.backend.set_image_data_format('channels_last')

def generateModel(output):
	model = tf.keras.Sequential([
		Conv2D(32, kernel_size=5, activation='relu', input_shape=(SPEC_MAX_WIDTH, SPEC_MAX_HEIGHT, 1)),
		BatchNormalization(),

		# Conv2D(48, kernel_size=4, activation='relu'),
		# BatchNormalization(),
		#
		# Conv2D(120, kernel_size=3, activation='relu'),
		# BatchNormalization(),

		MaxPooling2D(pool_size=(2, 2)),
		Dropout(0.25),

		Flatten(),

		Dense(64, activation='relu'),
		BatchNormalization(),
		Dropout(0.25),

		Dense(64, activation='relu'),
		BatchNormalization(),
		Dropout(0.4),

		Dense(output, activation='softmax')
	])

	# model = tf.keras.Sequential([
	# 	Dense(1, input_shape=(SPEC_MAX_WIDTH, SPEC_MAX_HEIGHT,)),
	# 	Flatten(),
	# 	Activation('relu'),
	# 	Dense(66, activation='relu'),
	# 	Dense(output, activation='softmax'),
	# ])

	model.compile(optimizer='adadelta',
				  loss='categorical_crossentropy',
				  metrics=['accuracy'])
	return model


if __name__ == '__main__':
	args = tfparser().parse_args()
	# extract command line arguments
	epochs = args.epochs

	# gather the files
	feature_files: List[FeatureFile] = list()
	for item in args.input:
		if isDirectory(item["name"]):
			files = FeatureDirectory(item["name"], item["label"]).getAllFiles()
			feature_files += files
		else:
			feature_files.append(FeatureFile(item["name"], item["label"]))

	# create the training and testing dataset
	x_train, x_test, y_train, y_test, encoder = generateDataset(feature_files)

	model = generateModel(len(encoder.classes_))
	model.summary()
	model.fit(x_train,
			  y_train,
			  epochs=epochs,
			  batch_size=200)
	loss, accuracy = model.evaluate(x_test, y_test)
	print(f"Accuracy: {accuracy * 100:.5f}")
	x = 1
