import os

try:
    import ujson as json
except:
    import json


class SearchManager:
    def __init__(self) -> None:
        # 读取全局变量
        self.path = 'data/ocg_bot/ocg_bot_search.json'
        self.search_type = 1
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
    def ReadSearchType(self, sessionId):
        try:
            return self.cfg[sessionId]['searchType']
        except KeyError:
            return self.search_type

    # --------------- 查询系统 结束 ---------------

    # --------------- 逻辑判断 开始 ---------------
    def CheckType(self, sessionId: str, userType: str = 'group'):
        searchType=self.ReadSearchType(sessionId)
        if searchType!=1 and searchType != 2 and searchType != 3:
            raise PermissionError(f'查询失败！')
        else:
            return searchType

    # --------------- 逻辑判断 结束 ---------------

    # --------------- 增删系统 开始 ---------------
    def UpdateSearchType(self, sessionId: str, type: int):
        if type != 1 and type != 2 and type!=3:
            return "请选择正确查卡方式"
        else:
            if not sessionId in self.cfg.keys():
                self.cfg[sessionId] = {}
            self.cfg[sessionId]['searchType'] = type
            self.WriteCfg()
            return f'查卡方式已更新为方法{type}'
        # --------------- 增删系统 结束 ---------------
