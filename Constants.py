import multiprocessing


# The sox tool may be installed anywhere on the computer
# So it's a bad idea to hard code its every use
SOX_PATH = "C:\\Program Files (x86)\\sox-14-4-2\\sox.exe"

SPEC_MAX_WIDTH, SPEC_MAX_HEIGHT = 256, 256

NO_CPU = multiprocessing.cpu_count()
