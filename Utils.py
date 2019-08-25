import argparse
import os
import re
import pathlib


def _readable_object(path):
	problem = None
	if os.path.exists(path):
		if os.access(path, os.R_OK):
			return path

		problem = "not accessible"
	problem = "not a valid location"

	raise argparse.ArgumentError(None, f"Path \"{path}\" is {problem}")


def _readable_directory(path):
	problem = None
	if os.path.exists(path):
		if os.path.isdir(path):
			if os.access(path, os.R_OK):
				return path

			problem = "not accessible"
		problem = "not a valid directory"
	problem = "not a valid location"

	raise argparse.ArgumentError(None, f"Path \"{path}\" is {problem}")


def _readable_file(path):
	problem = None

	if os.path.exists(path):
		if os.path.isfile(path):
			if os.access(path, os.R_OK):
				return path

			problem = "not accessible"
		problem = "not a valid file"
	problem = "not a valid location"

	raise argparse.ArgumentError(None, f"Path \"{path}\" is {problem}")


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


def listAllSubDirectories(path):
	return next(os.walk(path))[1]


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


def isPicture(filepath):
	_, extension = os.path.splitext(filepath)
	return extension in [".png", ".jpg"]


if __name__ == '__main__':
	f = "D:/Chrome downloads▬/101_ObjectCategories/101_ObjectCategories"
	x = listAllSubDirectories(f)
