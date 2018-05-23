# CustomVoice.AI 数据准备

## 目标

提供一个示例，帮助准备语音与文本数据，以便在基于微软Azure的[Custom Voice](https://customvoice.ai)上提交并训练自己的TTS模型。

## 数据格式

* 文本

  目前，需要用UTF-16LE编码文本文件。Windows上可以用Notepad另存为Unicode。常用的文本编辑器都有转换编码的功能，比如[Visual Studio Code](https://code.visualstudio.com)。对换行符并没有特定要求，经过试验，LF或CRLF都可以。

* 语音

  音频文件需要用PCM格式存储，扩展名为.wav，采样率16k，位深16-bit，单声道。用[MediaInfo](https://mediaarea.net/en/MediaInfo)可以看到如下参数:

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

  [FFmpeg](https://www.ffmpeg.org)可以用来转换和提取音频至PCM Wave，[SoX](http://sox.sourceforge.net)可以进一步规范格式。

```shell
ffmpeg -i sourcemedia.mp4 targetaudio.wav
sox targetaudio.wav -c 1 -r 16000 -b 16 00001.wav --norm -R
```

## 目录结构

建议分批组织和上传数据。上传文件的大小有限制，目前一批上传的录音最好不超过两个小时。模型训练的时候可以选择多批数据，只要没有重复ID。

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

`text_batch1.txt`的内容如下：

```text
01001	这是第一句话。
01002	这是最后一句话吗？
```

ID要和声音文件的文件名一致（不带扩展名），ID与文本之间要有一个制表符（不能是空格或者几个空格）。

上传的压缩文件里不能有任何目录，空目录也不行。建议使用[7-Zip](https://www.7-zip.org)，可以在每一批声音的文件夹里运行命令：`cd batch1 && 7z a batch1.zip *.wav`

## 其它处理

如果一个音频文件对应了很多句话，建议事先把音频按照句子切割，可参考[advanced](code/README.md)
