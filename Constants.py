import multiprocessing

# The sox tool may be installed anywhere on the computer
# So it's a bad idea to hard code its every use
SOX_PATH = "C:\\Program Files (x86)\\sox-14-4-2\\sox.exe"

TRAIN_TEST_RATIO = 0.95

SPEC_MAX_WIDTH, SPEC_MAX_HEIGHT, SPEC_NUM_CHANNELS = 128, 128, 1

NO_CPU = multiprocessing.cpu_count()

MODEL_ARCHITECTURE_SAVE_NAME = "model_architecture"
MODEL_ARCHITECTURE_SAVE_EXTENSION = "json"
MODEL_WEIGHTS_SAVE_NAME = "checkpoint"
MODEL_WEIGHTS_SAVE_EXTENSION = "hdf5"
ENCODER_SAVE_NAME = "encodings"
ENCODER_SAVE_EXTENSION = "codes"
