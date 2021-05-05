
from ._gacha import Gacha
from nonebot import on_command
from nonebot.adapters.cqhttp import Event, Bot,Message


GuardianTalesGacha1 = on_command("坎游单抽")
GuardianTalesGacha10 = on_command("坎游十连")
GuardianTalesGacha100 = on_command("坎游百连")
GuardianTalesGacha300 = on_command("坎游三百连")


@GuardianTalesGacha1.handle()
async def _(bot: Bot, event: Event):
    mes = Gacha().gacha_1()
    await GuardianTalesGacha1.finish(message=Message(mes))


@GuardianTalesGacha10.handle()
async def _(bot: Bot, event: Event):
    mes = Gacha().gacha_10()
    await GuardianTalesGacha10.finish(message=Message(mes))


@GuardianTalesGacha100.handle()
async def _(bot: Bot, event: Event):
    mes = Gacha().gacha_10(100)
    await GuardianTalesGacha100.finish(message=Message(mes))



@GuardianTalesGacha300.handle()
async def _(bot: Bot, event: Event):
    mes = Gacha().gacha_10(300)
    await GuardianTalesGacha300.finish(message=Message(mes))




