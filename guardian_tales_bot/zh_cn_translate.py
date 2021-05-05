
# 把中文名称转换成英语名称


import os
import json


FILE_PATH = os.path.dirname(__file__)
CHARACTERS_NAME = {}
ITEMS_NAME = {}




def load_name_json():
    # 读取保存名字的json文件
    global CHARACTERS_NAME
    global ITEMS_NAME

    with open(os.path.join(FILE_PATH, 'characters_name.json'), 'r', encoding='UTF-8') as f:
        CHARACTERS_NAME = json.load(f)

    with open(os.path.join(FILE_PATH, 'items_name.json'), 'r', encoding='UTF-8') as f:
        ITEMS_NAME = json.load(f)


load_name_json()




def character_name_translate(cn_name:str) ->str :
    # 根据角色中文名查找英文名称，遍历CHARACTERS_NAME来查找,找不到抛出异常

    for en_name in CHARACTERS_NAME.keys():
        if cn_name in CHARACTERS_NAME[en_name]:
            return en_name

    raise IndexError(f"找不到 {cn_name} 对应的英文名称，请检查是否中文输入错误或者characters_name.json文件有没有你输入的名字")


def item_name_translate(cn_name:str) ->str :
    # 根据物品中文名查找英文名称，在ITEMS_NAME查找,找不到抛出异常
    if cn_name in ITEMS_NAME :
        return ITEMS_NAME[cn_name]

    raise IndexError(f"找不到 {cn_name} 对应的英文名称，请检查是否中文输入错误或者items_name.json文件有没有你输入的名字")







