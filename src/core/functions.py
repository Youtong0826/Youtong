import discord
import json
import os
import re

def is_emoji(content:str):
    emoji_regexp = u'[\U00002600-\U000026FF]|[\U00002700-\U000027BF]|[\U0001f300-\U0001f5fF]|[\U0001f600-\U0001f64F]|[\U0001f680-\U0001f6FF]'
    result = []
    for chr in content:
        result += re.findall(emoji_regexp, chr, re.UNICODE)
        
    result += re.findall("<:\w+:\d+>|<\w+:\w+:\d+>",content)

    return False if len(result) == 0 else True

def load_extension(bot:discord.Bot, folder:str, mode:str="load", is_notice:bool=True) -> None:

    loading_method = {
        "load":bot.load_extension,
        "reload":bot.reload_extension,
        "unload":bot.unload_extension
    }

    if is_notice:
        print(f"Start {mode}ing {folder}")

    for Filename in os.listdir(f'src/{folder}'):
        if Filename.endswith(".py"):
            loading_method[mode](f"{folder}.{Filename[:-3]}")
            if is_notice:
                print(f'-- {mode}ed "{Filename}"')

    print(f"{mode}ing {folder} end")

    return None

def merge_dict(*dicts:dict) -> dict:
    raw = {}

    for d in dicts:
        raw.update(d)

    return raw

def read_json(path:str) -> dict:
    with open(path, "r", encoding="utf-8") as file:
        return json.loads(file.read())

def write_json(path:str, key:str, *value:dict, is_log:bool = True):
    new = original = read_json(path)
    new[key] = merge_dict(original.get(key,{}),*value)
    
    with open(path, "w", encoding="utf-8") as file:
        return file.write(json.dumps(
            new,
            indent=4,
            separators=(",",":"),
            ensure_ascii=False
        ))

if __name__ == "__main__":
    def test():                     #1038746334624231505
        print(is_emoji("<:Tenshi_cry:991664784682520667>"))
        print(is_emoji("<a:awoothink:9991059835047240500>"))
        print(is_emoji("hihi 😂🕐"))
        print(is_emoji("hihi"))

    def string_to_list(string):
        return str(list(string)).replace("'",'"')

    print(string_to_list("ㄅㄆㄇㄈㄉㄊㄋㄌㄍㄎㄏㄐㄑㄒㄔㄕㄖㄗㄘㄙㄧㄨㄩㄞㄛㄜㄝㄢㄟㄠㄡㄦㄣㄤㄥ"))
    print(string_to_list("0123456789"))
