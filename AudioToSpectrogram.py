# from src.Constants import SOX_PATH
from Utils import *
from Constants import SOX_PATH
from TimeStamp import TimeStamp
from Parser import setupParser
from math import ceil
import subprocess


def isAudioFile(filepath):
	command = f"{SOX_PATH} --i -t \"{filepath}\""
	child = subprocess.Popen(command, stdout=subprocess.PIPE)
	child.communicate()
	return bool(child.returncode)


def ConvertToSpectrogram(filepath, seconds=None, pieces=None, subdir=True):
	# get details about the file
	command = f"{SOX_PATH} --i \"{filepath}\""
	output = subprocess.check_output(command)
	details = soxiMatch(output)

	# decide how long the snapshots should be
	increment = 5000  # default is 5 seconds
	if seconds:
		increment = seconds * 1000
	if pieces:
		increment = (details["Samples"] // details["SampleRate"] // pieces) * 1000

	directory, name, ext = splitDirNameExt(filepath)
	# destination should look like: D:\Music\SongName\
	dest_dir = directory
	if subdir:
		dest_dir = buildDirPath(directory, name)
	makeDirectory(dest_dir)

	begin = TimeStamp(0)
	step = TimeStamp(increment)
	end = TimeStamp.parse(details["Duration"])
	i = 1
	pad = paddingZeros(ceil(end // step))
	# it does not matter if (step > end)
	while begin < end:
		for channel in range(1, details["Channels"] + 1):
			dest_file = buildDirPath(dest_dir, f"{name}_ch{channel}_part{i:0{pad}}.png")
			# -n (I don't know why, but it needs this flag)
			# remix {channel} (select a specific channel)
			# -S {begin} (process starting with the specified position)
			# -d {step} (duration of the segment)
			# -m (Spectrogram will be monochrome)
			# -r (Raw spectrogram: suppress the display of axes and legends)
			# -o (Name of the spectrogram output PNG file)
			command = f"\"{SOX_PATH}\" \"{filepath}\" -n " \
					  f"remix {channel} " \
					  f"spectrogram -S {begin} -d {step} -m -r -o \"{dest_file}\""
			subprocess.run(command)

		# increment stuff (note: in the main loop)
		begin.add(step)
		i += 1


if __name__ == '__main__':
	parser = setupParser()
	args = parser.parse_args()

	create_subdirectory = args.directory

	files = list()
	if args.input:
		for item in args.input:
			if isFile(item):
				files.append(item)
			elif isDirectory(item):
				files.extend(listDirectory(item))

	for file in files:
		print(f"Now processing \"{file}\"")
		ConvertToSpectrogram(file, subdir=create_subdirectory)
	print("All done")
