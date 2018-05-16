# Data preparation for CustomVoice.AI

## Goal

Provide a working end-to-end sample process of how to prepare data for [Custom Voice](https://customvoice.ai). Target audience: developers that are not quite familiar with audio processing.

## Data formats

* Text

  Text files should be saved with UTF-16 little endian encoding at the moment. Most modern text editor should be able to handle this. Take [Visual Studio Code](https://code.visualstudio.com) as an example. Bring up `Command Pallette` in `View` menu item (shortcut: `⇧⌘P` or `Ctrl+Shift+P`), type in `Change File Encoding`, select `Save with Encoding`, then `UTF-16 LE`. UTF-8 with or without BOM would be supported in future but not working yet.

* Audio

  Audio files should be saved as 16k sampling rate 16-bit depth mono PCM wave with .wav extension. Typical format information as viewed in [MediaInfo](https://mediaarea.net/en/MediaInfo):

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

It's likely that the audio files and correspondent text scripts are collected and organized per batch.

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

This basic guide assumes each wave contains one sentence (so the text is also one sentence per line). If you have only a big media file with many sentences, it should be pre-processed. See [advanced](code/README.md) for hints.
