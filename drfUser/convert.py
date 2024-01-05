from pypinyin import pinyin, Style


def convert_to_pinyin(name):
    pinyin_list = pinyin(name, style=Style.NORMAL)
    pinyin_string = "".join([item[0] for item in pinyin_list])
    return pinyin_string
