from typing import List
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
from Utils import buildFilePath
from tensorflow.python.keras.models import load_model, model_from_json
from tensorflow.python.keras.layers \
	import Dense, Flatten, Activation, \
	Conv2D, Dropout, BatchNormalization, MaxPooling2D, InputLayer
from Constants import SPEC_MAX_WIDTH, SPEC_MAX_HEIGHT, SPEC_NUM_CHANNELS, \
	MODEL_ARCHITECTURE_SAVE_NAME, MODEL_ARCHITECTURE_SAVE_EXTENSION, \
	MODEL_WEIGHTS_SAVE_NAME, MODEL_WEIGHTS_SAVE_EXTENSION, \
	ENCODER_SAVE_NAME, ENCODER_SAVE_EXTENSION


class MyModel:
	def __init__(self):
		self._model: tf.keras.Model = None
		self._encoder: LabelEncoder = None
		self._saveDirectory = None

	# <editor-fold desc="Get/Set Model">
	def createNew(self, output):
		self.model = MyModel.generateModel(output)

	def getinstance(self) -> tf.keras.Model:
		if self.model is None:
			raise Exception("No model. Load or create a new model first")
		return self.model

	# </editor-fold>

	# <editor-fold desc="Get/Set Encoder">
	def getEncoder(self):
		return self._encoder

	def setEncoder(self, encoder: LabelEncoder):
		self._encoder = encoder

	# </editor-fold>

	# <editor-fold desc="Get/Set SaveDirectory">
	def getSaveDirectory(self):
		return self._saveDirectory

	def setSaveDirectory(self, directory):
		self._saveDirectory = directory

	# </editor-fold>

	def decode(self, codes: List[List[float]]):
		if self._encoder is None:
			raise Exception("No LabelEncoder provided")

		# compute the maximum of each sublist
		codes = np.argmax(codes, axis=1)
		labels = self._encoder.inverse_transform(codes)
		return labels

	def savingEnabled(self):
		return self._saveDirectory is not None

	# <editor-fold desc="Saving / Loading model">
	# <editor-fold desc="Save/Load Encoder">
	def saveEncoder(self, directory=None):
		if self._encoder is None:
			raise Exception("No LabelEncoder provided")

		path = self._get_encoder_save_file_name(directory)
		with open(path, 'w') as f:
			for item in self._encoder.classes_.tolist():
				f.write("%s\n" % item)

	def loadEncoder(self, directory=None):
		path = self._get_encoder_save_file_name(directory)
		self._encoder = LabelEncoder()
		with open(path) as f:
			items = [line.rstrip('\n') for line in f]
			self._encoder.classes_ = np.array(items)


	# </editor-fold>

	# <editor-fold desc="Save/Load Architecture">
	def saveModelArchitecture(self, directory=None):
		if self.model is None:
			raise Exception("No model to save. Load or create a new model first")
		path = self._get_architecture_save_file_name(directory)
		with open(path, mode="w") as file:
			file.write(self.model.to_json())

	def loadModelArchitecture(self, directory=None):
		path = self._get_architecture_save_file_name(directory)
		with open(path, mode="r") as file:
			contents = file.read()
			self.model = model_from_json(contents)

	# </editor-fold>

	# <editor-fold desc="Save/Load Weights">
	def saveModelWeights(self, directory=None):
		if self.model is None:
			raise Exception("No model to save. Load or create a new model first")
		path = self._get_weights_save_file_name(directory)
		self.model.save(path)

	def loadModelWeights(self, directory=None):
		path = self._get_weights_save_file_name(directory)
		self.model.load_weights(path)

	# </editor-fold>

	# <editor-fold desc="Helpers">
	def _get_architecture_save_file_name(self, directory):
		path = self._build_save_file(directory, MODEL_ARCHITECTURE_SAVE_NAME, MODEL_ARCHITECTURE_SAVE_EXTENSION)
		return path

	def _get_weights_save_file_name(self, directory):
		path = self._build_save_file(directory, MODEL_WEIGHTS_SAVE_NAME, MODEL_WEIGHTS_SAVE_EXTENSION)
		return path

	def _get_encoder_save_file_name(self, directory):
		path = self._build_save_file(directory, ENCODER_SAVE_NAME, ENCODER_SAVE_EXTENSION)
		return path

	def _build_save_file(self, directory, name, extension):
		if self._saveDirectory is not None:
			directory = self._saveDirectory

		if directory is None:
			raise Exception("No save directory set")

		path = buildFilePath(directory=directory,
							 name=name,
							 extension=extension)
		return path

	# </editor-fold>
	# </editor-fold>

	@staticmethod
	def generateModel(output):
		activation = 'relu'

		model = tf.keras.Sequential([
			Conv2D(16, kernel_size=7, padding='same', activation=activation,
				   input_shape=(SPEC_MAX_WIDTH, SPEC_MAX_HEIGHT, SPEC_NUM_CHANNELS)),
			BatchNormalization(),

			Conv2D(24, kernel_size=5, padding='same', activation=activation),
			MaxPooling2D(),

			Conv2D(32, kernel_size=3, padding='same', activation=activation),
			MaxPooling2D(),

			Dropout(0.25),
			Flatten(),

			Dense(64, activation=activation),
			Dropout(0.4),
			Dense(output, activation='softmax')
		])

		model.compile(optimizer='rmsprop',
					  loss='categorical_crossentropy',
					  metrics=['accuracy'])
		return model
