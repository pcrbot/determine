import os
import random
import time
from hoshino import R, Service, priv
from hoshino.typing import CQEvent, HoshinoBot


date = True


sv_help = '''
| 鉴定
- 鉴定
- 鉴定你@某人
'''.strip()

sv = Service(
    name='鉴定',  # 功能名
    use_priv=priv.NORMAL,  # 使用权限
    manage_priv=priv.ADMIN,  # 管理权限
    visible=True,  # False隐藏
    enable_on_default=True,  # 是否默认启用
    bundle='娱乐',  # 属于哪一类
    help_=sv_help  # 帮助文本
)


@sv.on_fullmatch(["帮助鉴定"])
async def bangzhu(bot, ev):
    await bot.send(ev, sv_help, at_sender=True)


folder = R.img("determine_img/").path


def format_msg(qq: int):
    random.seed(qq * (time.time() // (24 * 3600)) if date else 1)
    while True:
        filelist = os.listdir(folder)
        random.shuffle(filelist)
        for filename in filelist:
            if os.path.isfile(os.path.join(folder, filename)):
                return R.img("determine_img/", filename).cqcode


@sv.on_fullmatch(["鉴定"])
async def jian(bot, ev: CQEvent):
    uid = ev.user_id
    name = ev.sender['nickname']
    msg = format_msg(uid)
    await bot.send(ev, f'鉴定{name}为：{msg}')


@sv.on_prefix('鉴定你')
@sv.on_suffix('鉴定你')
async def self_jian(bot, ev: CQEvent):
    sid = None
    gid = ev.group_id
    for m in ev.message:
        if m.type == 'at' and m.data['qq'] != 'all':
            sid = int(m.data['qq'])
    if sid is None:
        await bot.finish(ev, '后面跟要鉴定的人～', at_sender=True)
    data1 = await bot.get_group_member_info(group_id=gid, user_id=sid)
    name = data1['card'] if len(data1['card']) != 0 else data1['nickname']
    msg = format_msg(sid)
    await bot.send(ev, f'鉴定{name}为：{msg}')
