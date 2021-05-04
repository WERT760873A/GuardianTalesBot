
from ._gacha import Gacha
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event


GuardianTalesGacha_10 = on_command("坎游抽卡",aliases={"坎游十连","十连"} ,rule=to_me(), priority=1)


@GuardianTalesGacha_10.handle()
async def _(bot: Bot, event: Event):
    mes = Gacha().gacha_10()
    await GuardianTalesGacha_10.send(message=mes)











