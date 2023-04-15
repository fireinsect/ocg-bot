import os
import random
import time

from src.libraries.globalMessage import random_sendwitchoutcd

try:
    import ujson as json
except:
    import json


class PermissionManager:
    def __init__(self) -> None:
        # 读取全局变量
        self.path = 'data/ocg_bot/ocg_bot_cfg.json'
        self.random_cd = 10
        self.random_cd = self.random_cd if self.random_cd > 0 else 0
        # 读取perm_cfg
        self.ReadCfg()

    def ReadCfg(self) -> dict:
        try:
            # 尝试读取
            with open(self.path, 'r', encoding='utf-8') as f:
                self.cfg = json.loads(f.read())
            return self.cfg
        except Exception as e:
            # 读取失败
            self.cfg = {}
            self.WriteCfg()
            return {}

    def WriteCfg(self):
        # 尝试创建路径
        os.makedirs(self.path[:-16], mode=0o777, exist_ok=True)
        # 写入数据
        with open(self.path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(self.cfg))

    # --------------- 文件读写 开始 ---------------

    # --------------- 查询系统 开始 ---------------
    # 查询上一次发送时间
    def ReadLastSend(self, sessionId):
        try:
            return self.cfg['last'][sessionId]
        except KeyError:
            return 0

        # 查询cd
    def ReadCd(self, group_sessionId):
        try:
            return self.cfg[group_sessionId]['cd']
        except KeyError:
            return self.random_cd
    # 查询黑名单
    def ReadBanList(self, sessionId):
        try:
            return sessionId in self.cfg['ban']
        except KeyError:
            return False

    # --------------- 查询系统 结束 ---------------

    # --------------- 逻辑判断 开始 ---------------
    def CheckPermission(self, sessionId: str,groupSession: str, userType: str = 'group'):
        if self.ReadBanList(groupSession):
            raise PermissionError(f'抽卡功能已关闭！')
        # 查询冷却时间
        if groupSession is None:
            timeLeft = self.ReadCd(sessionId) + self.ReadLastSend(sessionId) - time.time()
        else:
            timeLeft = self.ReadCd(groupSession) + self.ReadLastSend(sessionId) - time.time()
        if timeLeft > 0:
            hours, minutes, seconds = 0, 0, 0
            if timeLeft >= 60:
                minutes, seconds = divmod(timeLeft, 60)
                hours, minutes = divmod(minutes, 60)
            else:
                seconds = timeLeft
            cd_msg = f"{str(round(hours)) + '小时' if hours else ''}{str(round(minutes)) + '分钟' if minutes else ''}{str(round(seconds,3)) + '秒' if seconds else ''}"
            raise PermissionError(f"{random.choice(random_sendwitchoutcd)} 你的CD还有{cd_msg}！")
    # --------------- 逻辑判断 结束 ---------------

    # --------------- 冷却更新 开始 ---------------
    # 最后一次发送的记录
    def UpdateLastSend(self, sessionId):
        try:
            self.cfg['last'][sessionId] = time.time()
        except KeyError:
            self.cfg['last'] = {
                sessionId: time.time()
            }

    # --------------- 冷却更新 结束 ---------------

    # --------------- 增删系统 开始 ---------------

    # cd部分
    def UpdateCd(self, sessionId: str, cdTime: int):
        # 检查数据是否超出范围，超出则设定至范围内
        cdTime = cdTime if cdTime > 0 else 0
        # 读取原有数据
        try:
            cdTime_old = self.cfg[sessionId]['cd']
        except KeyError:
            cdTime_old = '未设定'
        # 写入新数据
        if sessionId not in self.cfg.keys():
            self.cfg[sessionId] = {}
            self.WriteCfg()
        self.cfg[sessionId]['cd'] = cdTime
        self.WriteCfg()
        # 返回信息
        return f'成功更新冷却时间 {cdTime_old} -> {cdTime}'

    def UpdateBanList(self, sessionId: str, add_mode: bool):
        # 加入黑名单
        if add_mode:
            try:
                if sessionId in self.cfg['ban']:
                    return f'功能已经关闭'
            except KeyError:
                self.cfg['ban'] = []
            self.cfg['ban'].append(sessionId)
            self.WriteCfg()
            return f'功能已经关闭'
        # 移出黑名单
        else:
            try:
                self.cfg['ban'].remove(sessionId)
                self.WriteCfg()
                return f'功能已经开启'
            except ValueError:
                return f'功能已经开启'
        # --------------- 增删系统 结束 ---------------
