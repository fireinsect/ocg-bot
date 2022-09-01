import os

try:
    import ujson as json
except:
    import json


class PermissionManager:
    def __init__(self) -> None:
        # 读取全局变量
        self.path = 'data/ocg_bot/ocg_bot_cfg.json'
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
    # 查询黑名单
    def ReadBanList(self, sessionId):
        try:
            return sessionId in self.cfg['ban']
        except KeyError:
            return False

    # --------------- 查询系统 结束 ---------------

    # --------------- 逻辑判断 开始 ---------------
    def CheckPermission(self, sessionId: str, userType: str = 'group'):
        if self.ReadBanList(sessionId):
            raise PermissionError(f'功能对 {sessionId} 禁用！')

    # --------------- 逻辑判断 结束 ---------------

    # --------------- 增删系统 开始 ---------------
    def UpdateBanList(self, sessionId: str, add_mode: bool):
        # 加入黑名单
        if add_mode:
            try:
                if sessionId in self.cfg['ban']:
                    return f'已在黑名单'
            except KeyError:
                self.cfg['ban'] = []
            self.cfg['ban'].append(sessionId)
            self.WriteCfg()
            return f'成功添加至黑名单'
        # 移出黑名单
        else:
            try:
                self.cfg['ban'].remove(sessionId)
                self.WriteCfg()
                return f'成功移出黑名单'
            except ValueError:
                return f'{sessionId}不在黑名单'
        # --------------- 增删系统 结束 ---------------
