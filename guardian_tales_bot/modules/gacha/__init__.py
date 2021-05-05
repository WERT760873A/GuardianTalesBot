
from ._gacha import Gacha
from nonebot import on_command
from nonebot.adapters.cqhttp import Event, Bot,Message



GuardianTalesGacha = on_command("坎游抽卡",aliases={"坎游单抽","坎游十连","坎游百连","坎游三百连"})



@GuardianTalesGacha.handle()
async def _(bot: Bot, event: Event):
    ev = event.get_message()
    print(ev)
    mes = Gacha().gacha_10()
    await GuardianTalesGacha.finish(message=Message(mes))











