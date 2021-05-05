
# 抽卡模块

from guardian_tales_bot.zh_cn_translate import character_name_translate,item_name_translate
from guardian_tales_bot.icon_handling import get_character_icon,get_item_icon,image_to_CQ_code,get_character_gacha_icon,get_arm_gacha_icon
from PIL import Image
import os
import json
import random
import math


FILE_PATH = os.path.dirname(__file__)

# 卡池数据
POOL = {
    "character":{
        "3_star_UP":[],
        "3_star_not_UP":[],
        "2_star":[],
        "1_star":[],

        "all_3_star":[]
    },

    "arms":{
        "5_star_exclusive_UP":[],
        "5_star_exclusive_not_UP":[],
        "4_star_exclusive":[],
        "5_star":[],
        "4_star":[],
        "3_star":[],
        "2_star":[],

        "all_exclusive_not_UP":[],
        "all_exclusive":[]
    }
}




def load_pool():
    # 读取config.json的数据，导入卡池
    global POOL

    with open(os.path.join(FILE_PATH, 'config.json'), 'r', encoding='UTF-8') as f:
        config = json.load(f)

        for key in config["character"].keys():
            POOL["character"][key] = config["character"][key]

        POOL["character"]["all_3_star"].extend(POOL["character"]["3_star_UP"])
        POOL["character"]["all_3_star"].extend(POOL["character"]["3_star_not_UP"])


        for key in config["arms"].keys():
            POOL["arms"][key] = config["arms"][key]

        POOL["arms"]["all_exclusive_not_UP"].extend(POOL["arms"]["5_star_exclusive_not_UP"])
        POOL["arms"]["all_exclusive_not_UP"].extend(POOL["arms"]["4_star_exclusive"])

        POOL["arms"]["all_exclusive"].extend(POOL["arms"]["all_exclusive_not_UP"])
        POOL["arms"]["all_exclusive"].extend(POOL["arms"]["5_star_exclusive_UP"])


load_pool()




class Gacha(object):
    def __init__(self,pool = "character", up=True):
        self.pool = pool
        self.up = up

        # 当前是多少抽
        self.current_times = 0

        # 抽卡结果统计
        self.gacha_count = {
            "1_star": 0,
            "2_star": 0,
            "3_star": 0,
            "4_star": 0,
            "5_star": 0,
            "exclusive":0}

        # 记录多少抽第一次出现4星或5星
        self.last_4 = 0
        self.last_5 = 0

        # 记录多少抽第一次出现UP
        self.last_up = 0

        # 需要生成图片的抽卡结果列表
        self.gacha_list = []

        # 角色4星和武器2星的十连保底计数,注意这个计数是从0开始的，每一次抽卡（包括第一次）之前都得+1
        self.character_4_star_must = 0
        self.arm_2_star_must = 0

        # 设置 self.gacha_list 是否保留 1星的抽卡结果，防止抽卡次数过多最后拼接的图太大，以下几个参数类似
        self.keep_1_star_im = True
        self.keep_2_star_im = True
        self.keep_3_star_im = True
        self.keep_4_star_im = True
        self.keep_5_star_im = True
        self.keep_exclusive_im = True



    def get_1_star(self) -> Image:
        # 随机一个1星的角色
        # 这里会直接把抽卡结果的图片放到 self.gacha_list 然后返回图片
        self.gacha_count["1_star"] += 1
        cn_name = random.choice(POOL[self.pool]["1_star"])
        en_name = character_name_translate(cn_name)
        im = get_character_gacha_icon(en_name,star=1)

        if self.keep_1_star_im:
            self.gacha_list.append(im)
        return im



    def get_2_star(self):
        # 随机一个2星角色或武器
        self.gacha_count["2_star"] += 1
        cn_name = random.choice(POOL[self.pool]["2_star"])

        if self.pool == "character":
            en_name = character_name_translate(cn_name)
            im = get_character_gacha_icon(en_name,star=2)

        else:
            en_name = item_name_translate(cn_name)
            im = get_arm_gacha_icon(en_name,star=2)

        if self.keep_2_star_im:
            self.gacha_list.append(im)

        return im




    def get_3_star(self):
        # 随机一个3星角色或武器
        self.gacha_count["3_star"] += 1

        # 这是武器池的情况
        if self.pool == "arms":
            cn_name = random.choice(POOL[self.pool]["3_star"])
            en_name = item_name_translate(cn_name)
            im = get_arm_gacha_icon(en_name,star=3)

            if self.keep_3_star_im:
                self.gacha_list.append(im)
            return im

        # 下边是角色池
        if self.up:
            if random.random() > 0.5:
                cn_name = random.choice(POOL[self.pool]["3_star_UP"])
            else:
                cn_name = random.choice(POOL[self.pool]["3_star_not_UP"])
        else:
            cn_name = random.choice(POOL[self.pool]["all_3_star"])
        en_name = character_name_translate(cn_name)
        im = get_character_gacha_icon(en_name,star=3)

        if self.keep_3_star_im:
            self.gacha_list.append(im)

        return im



    def get_4_star(self):
        # 随机一个4星装备
        self.gacha_count["4_star"] += 1
        cn_name = random.choice(POOL[self.pool]["4_star"])
        en_name = item_name_translate(cn_name)
        im = get_arm_gacha_icon(en_name,star=4)

        if self.keep_4_star_im:
            self.gacha_list.append(im)

        return im



    def get_5_star(self):
        # 随机一个5星装备，5星装备不包括专武
        self.gacha_count["5_star"] += 1
        cn_name = random.choice(POOL[self.pool]["5_star"])
        en_name = item_name_translate(cn_name)
        im = get_arm_gacha_icon(en_name,star=5)

        if self.keep_5_star_im:
            self.gacha_list.append(im)

        return im



    def get_exclusive(self):
        # 随机一个专属武器
        self.gacha_count["exclusive"] += 1

        if self.up:
            if random.random() > 0.5:
                cn_name = random.choice(POOL[self.pool]["5_star_exclusive_UP"])
            else:
                cn_name = random.choice(POOL[self.pool]["all_exclusive_not_UP"])
        else:
            cn_name = random.choice(POOL[self.pool]["all_exclusive"])

        en_name = item_name_translate(cn_name)
        im = get_arm_gacha_icon(en_name,star=5,exclusive=True)

        if self.keep_exclusive_im:
            self.gacha_list.append(im)

        return im



    def gacha_one_character(self):
        # 抽一次角色
        r = random.random()
        self.character_4_star_must += 1

        probability = 0.0275
        if r < probability:
            return self.get_3_star()

        probability += 0.19
        if (r < probability) or (self.character_4_star_must % 10 == 0):
            self.character_4_star_must = 0
            return self.get_2_star()

        return self.get_1_star()



    def gacha_one_arm(self):
        # 抽一次武器
        r = random.random()
        self.arm_2_star_must += 1

        probability = 0.03
        if r < probability:
            return self.get_exclusive()

        probability += 0.03
        if r < probability:
            return self.get_5_star()

        probability += 0.09
        if (r < probability) or (self.arm_2_star_must % 10 == 0):
            self.arm_2_star_must = 0
            return self.get_4_star()

        probability += 0.27
        if r <probability:
            return self.get_3_star()

        return self.get_2_star()


    def get_gacha_count(self):
        # 获取抽卡统计结果
        txt = ""

        if self.gacha_count['1_star']:
            txt += f"★×{self.gacha_count['1_star']}   "
        if self.gacha_count['2_star']:
            txt += f"★★×{self.gacha_count['2_star']}   "
        if self.gacha_count['3_star']:
            txt += f"★★★×{self.gacha_count['3_star']}   "
        if self.gacha_count['4_star']:
            txt += f"★★★★×{self.gacha_count['4_star']}   "
        if self.gacha_count['5_star']:
            txt += f"★★★★★×{self.gacha_count['5_star']}   "
        if self.gacha_count['exclusive']:
            txt += f"专属武器×{self.gacha_count['exclusive']}   "

        return txt


    def set_keep_im(self,frequency):
        # 设置不同星级的抽卡结果是否保留在 self.gacha_list

        if self.pool == "arms":
            # 这是武器池设置
            if frequency:
                if frequency >= 50:
                    self.keep_2_star_im = False
                if frequency >= 100:
                    self.keep_3_star_im = False

        else:
            # 这是角色池设置
            if frequency >= 50:
                self.keep_1_star_im = False
            if frequency >= 300:
                self.keep_2_star_im = False


    def gacha_list_splice(self):
        # 对 self.gacha_list 里的图片进行拼接，返回完整大图

        size = self.gacha_list[0].size
        w = int(size[0] * 5)
        h = int(size[1] * math.ceil(len(self.gacha_list) / 5))
        back = Image.new("RGBA",( w, h))
        for i in range(len(self.gacha_list)):
            im = self.gacha_list[i]
            x = size[0] * (i % 5)
            y = i // 5 * size[1]
            back.paste(im,( x, y))

        return back




    def gacha_1(self):
        #单抽

        if self.pool == "arms":
            self.gacha_one_arm()
        else:
            self.gacha_one_character()

        im = self.gacha_list[0]
        size = im.size
        im = im.resize((int(size[0] / 3), int(size[1] / 3)))
        mes = image_to_CQ_code(im)
        mes += "\n"
        mes += self.get_gacha_count()
        return mes


    def gacha_10(self,frequency=10):
        # 多次抽卡
        self.set_keep_im(frequency)

        for self.current_times in range(frequency):
            self.current_times  += 1

            if self.pool == "arms":
                self.gacha_one_arm()
            else:
                self.gacha_one_character()

        splice_im = self.gacha_list_splice()
        size = splice_im.size
        splice_im = splice_im.resize((int(size[0]/3),int(size[1]/3)))
        mes = image_to_CQ_code(splice_im)
        mes += "\n"
        mes += self.get_gacha_count()
        return mes

