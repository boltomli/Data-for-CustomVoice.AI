# 进阶数据处理

## 目标

处理特别的情况。

* 把一个包含很多句录音的媒体文件与文本对齐，以便切分为多个文件，每句对应一行文本。

## 对齐的参考实现

音视频文件应只包含人声，音效、音乐等需事先另行去除，可使用音频编辑软件，如[Audacity](https://www.audacityteam.org)。文本文件应只包含录音的脚本，没有ID等额外信息，建议每句一行。成功安装和使用[Aeneas](https://github.com/readbeyond/aeneas)需要[espeak](https://sourceforge.net/projects/espeak/)。

```shell
virtualenv venv
source venv/bin/activate
pip install jupyter numpy
pip install git+https://github.com/readbeyond/aeneas@devel
jupyter notebook
```
