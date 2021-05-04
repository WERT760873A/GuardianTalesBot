
# 抽卡模块

from ..zh_cn_translate import character_name_translate,item_name_translate
from ..icon_handling import get_character_icon,get_item_icon,image_to_CQ_code,get_character_gacha_icon,get_arm_gacha_icon
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

        # 保底计数,注意这个计数是从0开始的，每一次抽卡（包括第一次）之前都得+1
        self.distance_4_star = 0



    def get_1_star(self) -> Image:
        # 随机一个1星的角色
        # 这里会直接返回抽卡结果的图片
        self.gacha_count["1_star"] += 1
        name = random.choice(POOL[self.pool]["1_star"])
        return get_character_gacha_icon(name,star=1)



    def get_2_star(self):
        # 随机一个2星角色或武器
        self.gacha_count["2_star"] += 1
        name = random.choice(POOL[self.pool]["2_star"])

        if self.pool == "character":
            return get_character_gacha_icon(name,star=2)
        else:
            return get_arm_gacha_icon(name,star=2)




    def get_3_star(self):
        # 随机一个3星角色或武器
        self.gacha_count["3_star"] += 1

        # 这是武器池的情况
        if self.pool == "arms":
            name = random.choice(POOL[self.pool]["3_star"])
            return get_arm_gacha_icon(name,star=3)

        # 下边是角色池
        if self.up:
            if random.random() > 0.5:
                name = random.choice(POOL[self.pool]["3_star_UP"])
            else:
                name = random.choice(POOL[self.pool]["3_star_not_UP"])
        else:
            name = random.choice(POOL[self.pool]["all_3_star"])
        return get_character_gacha_icon(name,star=3)



    def get_4_star(self):
        # 随机一个4星装备
        self.gacha_count["4_star"] += 1
        name = random.choice(POOL[self.pool]["4_star"])
        return get_arm_gacha_icon(name,star=4)



    def get_5_star(self):
        # 随机一个5星装备，5星装备不包括专武
        self.gacha_count["5_star"] += 1
        name = random.choice(POOL[self.pool]["5_star"])
        return get_arm_gacha_icon(name,star=5)



    def get_exclusive(self):
        # 随机一个专属武器
        self.gacha_count["exclusive"] += 1

        if self.up:
            if random.random() > 0.5:
                name = random.choice(POOL[self.pool]["5_star_exclusive_UP"])
            else:
                name = random.choice(POOL[self.pool]["all_exclusive_not_UP"])
        else:
            name = random.choice(POOL[self.pool]["all_exclusive"])

        return get_arm_gacha_icon(name,star=5,exclusive=True)



    def gacha_one_character(self):
        # 抽一次角色
        r = random.random()

        probability = 0.0275
        if r < probability:
            return self.get_3_star()

        probability += 0.19
        if (r < probability) or (self.current_times % 10 == 0):
            return self.get_2_star()

        return self.get_1_star()



    def gacha_one_arm(self):
        # 抽一次武器
        r = random.random()

        probability = 0.03
        if r < probability:
            return self.get_exclusive()

        probability += 0.03
        if r < probability:
            return self.get_5_star()

        probability += 0.09
        if (r < probability) or (self.current_times % 10 == 0):
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
            im = self.gacha_one_arm()
        else:
            im = self.gacha_one_character()

        mes = image_to_CQ_code(im)
        mes += "\n"
        mes += self.get_gacha_count()
        return mes


    def gacha_10(self):
        # 10连
        for self.current_times in range(10):
            self.current_times  += 1

            if self.pool == "arms":
                im = self.gacha_one_arm()
            else:
                im = self.gacha_one_character()

            self.gacha_list.append(im)

        splice_im = self.gacha_list_splice()
        size = splice_im.size
        splice_im = splice_im.resize((int(size[0]/2),int(size[1]/2)))
        mes = image_to_CQ_code(splice_im)
        mes += "\n"
        mes += self.get_gacha_count()
        return mes

