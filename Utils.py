import argparse
import os
import re
import pathlib


def _readable_object(path):
	if not os.path.exists(path):
		raise argparse.ArgumentError(None, f"Path \"{path}\" is not a valid file or directory")

	if os.access(path, os.R_OK):
		return path

	else:
		raise argparse.ArgumentError(None, f"Object \"{path}\" exists, but is not accessible")


def isFile(path):
	return os.path.isfile(path)


def isDirectory(path):
	return os.path.isdir(path)


def listDirectory(path):
	items = list()
	for root, _, files in os.walk(path):
		for f in files:
			items.append(buildDirPath(root, f))
	return items


def splitPath(filepath):
	filepath = os.path.normpath(filepath)
	directory, filename = os.path.split(filepath)
	return directory, filename


def splitFile(filename):
	name, extension = os.path.splitext(filename)
	return name, extension


def splitDirNameExt(filepath):
	filepath = os.path.normpath(filepath)
	directory, name = os.path.split(filepath)
	name, ext = os.path.splitext(name)
	return directory, name, ext


def buildFilePath(directory, name, extension):
	dot = '.' if extension[0] == '.' else '.'
	return os.path.join(directory, f"{name}{dot}{extension}")


def buildDirPath(*args):
	newpath = os.path.join(*args)
	return os.path.normpath(newpath)


def makeDirectory(path):
	pathlib.Path(path).mkdir(parents=True, exist_ok=True)


def paddingZeros(value: int):
	digits = 0
	while value:
		value = value // 10
		digits += 1
	return digits


def soxiMatch(string):
	pattern = re.compile(br".*Input File\s*:\s*'(.*)'.*"
						 br"Channels\s*:\s*(\d+).*"
						 br"Sample Rate\s*:\s*(\d+).*"
						 br"Precision\s*:\s*(\d+).*"
						 br"Duration\s*:\s*(\d+:\d+:\d+.\d+)\s=\s(\d+)\ssamples",
						 flags=re.MULTILINE | re.DOTALL)
	result = pattern.match(string)

	if result:
		values = {"FileName": result.group(1).decode(),
				  "Channels": int(result.group(2)),
				  "SampleRate": int(result.group(3)),
				  "SampleSize": int(result.group(4)),
				  "Duration": result.group(5).decode(),
				  "Samples": int(result.group(6))}
		return values
	else:
		raise Exception("Invalid format")


def timestampMatch(string):
	pattern = re.compile(r"\s*(?:(\d+):)?(?:(\d+):)?(?:(\d+)[.,:])?(\d+)\s*")
	result = pattern.match(string)
	if result:
		hours = result.group(1) or 0
		minutes = result.group(2) or 0
		seconds = result.group(3) or 0
		milliseconds = result.group(4)
		values = {"Hours": int(hours),
				  "Minutes": int(minutes),
				  "Seconds": int(seconds),
				  "Milliseconds": int(milliseconds)}
		return values
	else:
		raise Exception("Invalid format")


def getImageData(filepath):
	with open(filepath, 'rb') as img:
		return img.read()


if __name__ == '__main__':
	f = "D:/WAV files/fisiere/ABBA - unknown album - 00 - Dancing Queen/ABBA - unknown album - 00 - Dancing Queen_ch1_part01.png"
	x = getImageData(f)
