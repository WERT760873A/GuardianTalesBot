
# 图标处理模块
from .zh_cn_translate import character_name_translate,item_name_translate

from PIL import Image
from io import BytesIO
import os
import json
import base64

FILE_PATH = os.path.dirname(__file__)
ICON_PATH = os.path.join(FILE_PATH,'icon')

CHARACTERS = {}
ITEMS = {}
PORTRAITS = {}

character_back_icon = {
    "1":Image.open(os.path.join(ICON_PATH, 'character_star_1.png')),
    "2":Image.open(os.path.join(ICON_PATH, 'character_star_2.png')),
    "3":Image.open(os.path.join(ICON_PATH, 'character_star_3.png'))
    }

arm_star_icon = {
    "1":Image.open(os.path.join(ICON_PATH, 'arm_star_1_1.png')),
    "2":Image.open(os.path.join(ICON_PATH, 'arm_star_2_2.png')),
    "3":Image.open(os.path.join(ICON_PATH, 'arm_star_3_3.png')),
    "4":Image.open(os.path.join(ICON_PATH, 'arm_star_4_4.png')),
    "5":Image.open(os.path.join(ICON_PATH, 'arm_star_5_5.png')),
    "exclusive":Image.open(os.path.join(ICON_PATH, 'slot_only_mark.png'))
    }

def load_json():
    # 载入icon文件夹的3个json和图标
    global CHARACTERS
    global ITEMS
    global PORTRAITS

    with open(os.path.join(ICON_PATH, 'characters.json'), 'r', encoding='UTF-8') as f:
        for character in json.load(f):
            name = character["name"]
            CHARACTERS[name] = character
    CHARACTERS["icon"] = Image.open(os.path.join(ICON_PATH, 'characters.png'))

    with open(os.path.join(ICON_PATH, 'items.json'), 'r', encoding='UTF-8') as f:
        for item in json.load(f):
            name = item["name"]
            ITEMS[name] = item
    ITEMS["icon"] = Image.open(os.path.join(ICON_PATH, 'items.png'))

    with open(os.path.join(ICON_PATH, 'portraits.json'), 'r', encoding='UTF-8') as f:
        for portrait in json.load(f):
            name = portrait["name"]
            PORTRAITS[name] = portrait
    PORTRAITS["icon"] = Image.open(os.path.join(ICON_PATH, 'portraits.png'))


load_json()



def get_character_icon(name:str,star=3) ->Image :
    # 这个函数返回的是角色的全身像素图
    # 根据名字返回裁切好的图标,这里的 name 只能使用英文名称
    # 角色不同的星级有不同的像素图，这里默认返回3星的,
    # 调用时指定 star 的参数可以返回其他星级的图片，注意初始2星没有1星的图，初始3星没有1星和2星的图
    # 游戏里的图标有大有小，返回的 Image 的图片尺寸不是固定的

    if str(star) != "1":
        name = f"{name}_{star}"

    x = CHARACTERS[name]["x"]
    y = CHARACTERS[name]["y"]
    w = CHARACTERS[name]["width"]
    h = CHARACTERS[name]["height"]
    return CHARACTERS["icon"].crop((x, y, x + w, y + h))



def get_item_icon(name:str) ->Image :
    # 这个函数返回游戏中物品的图标
    x = ITEMS[name]["x"]
    y = ITEMS[name]["y"]
    w = ITEMS[name]["width"]
    h = ITEMS[name]["height"]
    return ITEMS["icon"].crop((x, y, x + w, y + h))


def get_portrait_icon(name:str) ->Image :
    # 这个函数返回角色的头像，不是全身像素图
    x = PORTRAITS[name]["x"]
    y = PORTRAITS[name]["y"]
    w = PORTRAITS[name]["width"]
    h = PORTRAITS[name]["height"]
    return PORTRAITS["icon"].crop((x, y, x + w, y + h))




def icon_zoom(im:Image, box=(50,50)) ->Image :
    # 在长宽比不变的情况下对图像进行缩放，用来统一图标的尺寸
    # 传入的 box 参数为最终返回的图像尺寸大小
    size = im.size
    width_ratio = box[0]/size[0]
    height_ratio = box[1]/size[1]

    zoom = min(width_ratio,height_ratio)
    new_width = int(size[0] * zoom)
    new_height = int(size[1] * zoom)
    im = im.resize((new_width,new_height))

    new_im = Image.new("RGBA",box)
    x = (box[0] / 2) - (new_width / 2)
    y = (box[1] / 2) - (new_height / 2)
    new_im.paste(im, (int(x), int(y)), im)

    return new_im




def image_to_CQ_code(im:Image) ->str :
    # image对象转CQ码
    bio = BytesIO()
    im.save(bio, format='PNG')
    base64_str = base64.b64encode(bio.getvalue()).decode()
    return f"[CQ:image,file=base64://{base64_str}]"



def get_character_gacha_icon(en_name:str,star=3) -> Image :
    # 返回角色的抽卡结果图

    character_icon = get_character_icon(en_name,star=star)
    back = character_back_icon[str(star)].copy()
    character_icon = icon_zoom(character_icon, (130, 140))
    back.paste(character_icon, (21, 48), character_icon)

    return back



def get_arm_gacha_icon(en_name:str,star=3,exclusive=False) -> Image :
    # 返回装备抽卡结果图

    arm_icon = get_item_icon(en_name)
    back = arm_star_icon[str(star)].copy()
    character_icon = icon_zoom(arm_icon, (90, 90))
    back.paste(character_icon, (42, 68), character_icon)

    if exclusive:
        exclusive_icon = arm_star_icon["exclusive"]
        back.paste(exclusive_icon,(121,64),exclusive_icon)

    return back







