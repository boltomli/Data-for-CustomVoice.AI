# Interval Converter

## Usage

```shell
pip install -r requirements.txt
python interval-converter.py --help
```

## 例子：标贝科技中文标准女声音库

### 10000句下载

<http://www.data-baker.com/open_source.html>

### 标注格式

1. 文本标注为 .txt 格式文档
1. 音节音素边界切分文件为 .interval 格式

### 处理过程

1. 用 `text-encoding-converter` 把 `ProsodyLabeling` 的文本从 GB2312 转换为 UTF-8
1. 运行 `python3 interval-converter.py PhoneLabeling/000003.interval result`

`ProsodyLabeling` 中的拼音标注与 `PhoneLabeling` 中声母韵母的格式不完全相同，还需要转换才能把两者对应起来。这里只是初步示例。
