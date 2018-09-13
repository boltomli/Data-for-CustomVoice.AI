# Advances data processing

## Goal

Given a big audio file and the text scripts, show a way to split the audio to small pieces according to text segments (forced alignment).

## Data

One audio file and the text scripts with only speech part in it. Better keep just one sentence per line.

If no data at hand, try the example from [Aeneas repo](https://github.com/readbeyond/aeneas/tree/devel) or grab one from [LibriVox](https://librivox.org).

## Usage

Run in Python 3 virtualenv is recommended. Install espeak development files first if there's error installing aeneas. Once the forced alignment is generated, you can split the audio according to the time information.

There is also an example to handle audio without text (do segmentation and ASR before alignment). Be aware that the quality is not guaranteed by default.

```shell
virtualenv venv
source venv/bin/activate
pip install jupyter numpy ffmpy SpeechRecognition
pip install git+https://github.com/readbeyond/aeneas@devel
jupyter notebook
```
