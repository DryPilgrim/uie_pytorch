#coding:utf-8
import sys

from uie_predictor import UIEPredictor
from pprint import pprint

# body="2月8日上午北京冬奥会自由式滑雪女子大跳台决赛中中国选手谷爱凌以188.25分获得金牌！"
# schema = [{'电视剧':['演员','时间']},'集数', '主演']  # 实体、关系抽取
# body="《康熙王朝》是2001年中国大陆拍摄的一部大型历史电视连续剧, 是由导演陈家林、刘大印执导, 陈道明、斯琴高娃、薛中锐、高兰村、茹萍、李建群、廖京生等人主演。原名《康熙帝国》，一共50集。它是在二月河的小说《康熙大帝》的基础上改编的，其背景故事是清朝世祖顺治帝的末年和圣祖康熙帝在位时的事迹。该剧从顺治皇帝哀痛爱妃董鄂妃病故时讲起，直至康熙在位61年驾崩而止。第一次以正剧的角度浓墨重彩刻画了清朝初期康熙皇帝充满传奇的一生。"

schema = ['用户', '粉丝数']
with open('html/ask.zol.com.cn.txt',encoding='utf-8') as f:
    body = f.read()
print(body)
ie = UIEPredictor(model='uie-base', schema=schema)
pprint(ie(body)) # Better print results using pprint