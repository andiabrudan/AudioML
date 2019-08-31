# AudioML

Named "AudioML" because initially it was supposed to classify sounds, this application has since been developed to classify small image files because of the necessity to first convert the audio files into spectrograms of manageable sizes.

## Getting Started

First off, set up a new python virtual environment where to install dependencies.

### Prerequisites
#### Library Dependencies
I've included a "dependencies.txt" file to give a perspective on all libraries used (gathered with "pip freeze"), but not all of them are necessary. To get up to date, you will need to install:
- numpy=1.16.4 (using later versions, a lot of warnings will be issued because of tensorflow)
- tensorflow==1.14.0 / tensorflow-gpu==1.14.0 (the gpu version takes advantage of CUDA, if the graphics card is compatible, but should revert to CPU otherwise)
- sklearn

The tensorflow library should install a lot of other dependencies it needs.

#### Sound eXchange
As previously mentioned, the application must first convert audio files to spectrograms to work correctly. To that end, SoundExchange (sox) will be needed.

To install this application, go to the [sox website](http://sox.sourceforge.net/), download the application and install it.

Now that sox is installed, the application needs to know the location of the executable. To specify it, open "Constants.py" and modify SOX_PATH to point to the correct location of the executable.


### Converting the files to spectrograms
To convert files, I've written a small python script that uses Sound eXchange to convert audio files. It can be used from the command line.

To see all options available run
```
AudioToSpectrogram.py -h
```
The general use case is
```
AudioToSpectrogram.py -d -s 5 -i "directory"
```

## Predicting some files
I've included a pre-trained model in NumbersModel that is able to accurately classify numbers spoken out loud.

For training, I've used the following [dataset](https://github.com/Jakobovski/free-spoken-digit-dataset)

To predict, it is first necessary to convert the sound files to spectrograms as described above, then use "tfmain.py" in predict mode:
```
tfmain.py --load "./NumbersModel/" predict -i "directory/to/files/"
```
To note: the spectrograms should be placed in a separate directory after conversion, otherwise tfmain.py will also read the audio files which will cause an error

## Training a model
If the tool is needed to train a new model, it should be run in train mode:
```
tfmain.py --save "save/location/" train -i "directory/to/files" NULL
```
To more easily train on datasets which have the following format:
```
directory/to/files/
├── class 1/
│   ├── img1.png
│   ├── img2.png
│   ├── img3.png
│   └── img4.png
├── class 2/
│   ├── img1.png
│   └── img2.png
└── class 3/
    ├── img1.png
    ├── img2.png
    ├── img3.png
    └── img4.png
```
I've included a special use case in the arguments parser: if a single directory is provided, the subdirectories inside become the class name for their respective files. That is the reason the previous command specified NULL as the label.

The general use case would be the following:
```
tfmain.py train -i "dir1/" dog -i "dir2/" cat -i "file.png" bird
```
