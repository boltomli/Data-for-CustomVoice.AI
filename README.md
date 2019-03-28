# Data preparation for CustomVoice.AI

## Goal

Provide a working end-to-end sample process of how to prepare data for [Custom Voice](https://customvoice.ai) powered by Microsoft Azure Cognitive Services. Target audience: developers that are not quite familiar with audio processing.

[中文版文档 for Chinese version](https://github.com/boltomli/Data-for-CustomVoice.AI/tree/cjk)

## Data formats

* Text

  Text files can be in most common encoding methods now as Azure custom voice service is updated. For examples, UTF-8/UTF-16LE/UTF-8 with BOM. Most modern text editor should be able to handle this. Take [Visual Studio Code](https://code.visualstudio.com) as an example. Bring up `Command Palette` in `View` menu item (shortcut: `⇧⌘P` or `Ctrl+Shift+P`), type in `Change File Encoding`, select `Save with Encoding`, then `UTF-16 LE`.

* Audio

  Audio files should be saved as at least 16k sampling rate 16-bit depth mono PCM wave with .wav extension. Waves with higher sampling rate can be uploaded now to the portal. Typical format information as viewed in [MediaInfo](https://mediaarea.net/en/MediaInfo):

```text
Format                                   : PCM
Format settings                          : Little / Signed
Codec ID                                 : 1
Duration                                 : 8 s 255 ms
Bit rate mode                            : Constant
Bit rate                                 : 256 kb/s
Channel(s)                               : 1 channel
Sampling rate                            : 16.0 kHz
Bit depth                                : 16 bits
Stream size                              : 258 KiB (100%)
```

  If collected audio is in other formats, [FFmpeg](https://www.ffmpeg.org) and [SoX](http://sox.sourceforge.net) will be helpful in conversion.

```shell
ffmpeg -i sourcemedia.mp4 targetaudio.wav
sox targetaudio.wav -c 1 -r 16000 -b 16 00001.wav --norm -R
```

## Data structure

It's recommended that the audio files and correspondent text scripts are collected and organized per batch. This way the uploading of each batch can be faster and it'll be easier to identify and fix issues. It'll also enable custom voice model creation using different sets of data. Multiple data sets selection is supported so if there's no overlap between batches, you can still use all the data for one model.

Find a few common issues against the requirement and code to help match ID and create zip files [here](code/batch-maker/README.md).

```text
.
├── batch1
│   ├── 01001.wav
│   ├── 01002.wav
├── batch2
│   ├── 02001.wav
│   ├── 02002.wav
│   └── 02003.wav
│   └── 02004.wav
├── batch3
│   ├── 01001.wav
│   ├── 03002.wav
│   └── 03003.wav
├── text_batch1.txt
├── text_batch2.txt
└── text_batch3.txt
```

Content of `text_batch1.txt` is like:

```text
01001	Text of the first sentence is here.
01002	Is this the last sentence of the batch?
```

Note that the ID in text must match the wave file name without extension. Between ID and sentence there is a `Tab` but not spaces. There should be exactly one `Tab` in each line.

Archive files to upload should contain wave files only. Take [7-Zip](https://www.7-zip.org) as an example, run the command in each batch folder `cd batch1 && 7z a batch1.zip *.wav`.

## Advanced data processing

This basic guide assumes each wave contains one sentence (so the text is also one sentence per line). If you have only a big media file with many sentences, it should be preprocessed. See [advanced](code/README.md) for hints.

## Suggestions or requests

[![Feature Requests](http://feathub.com/boltomli/Data-for-CustomVoice.AI?format=svg)](http://feathub.com/boltomli/Data-for-CustomVoice.AI)
