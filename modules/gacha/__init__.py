
from ._gacha import Gacha
from nonebot import on_command
from nonebot.adapters.cqhttp import Event, Bot, Message



GuardianTalesGacha_10 = on_command("坎游抽卡",aliases={"坎游十连","十连"})


@GuardianTalesGacha_10.handle()
async def _(bot: Bot, event: Event):
    mes = Gacha().gacha_10()
    await GuardianTalesGacha_10.finish(message=Message(mes))











