import time

from rqalpha.events import EVENT

from rqalpha.const import PERSIST_MODE
from rqalpha.interface import AbstractMod
from rqalpha.mod.rqalpha_mod_dib_persist.db_persist_provider import DBPersistProvider


class DIBPersistMod(AbstractMod):

    def __init__(self):
        self._mod_config = None
        self.provider = None

    def start_up(self, env, mod_config):
        self._mod_config = mod_config
        self._mod_config.env = env
        self._mod_config.run_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        self._mod_config.base = env.config.base

        env.config.base.persist = True
        env.config.base.persist_mode = PERSIST_MODE.ON_NORMAL_EXIT
        env.event_bus.add_listener(EVENT.POST_SYSTEM_INIT, self._init)


    def _init(self, event):
        env = self._mod_config.env
        self.provider = DBPersistProvider(self._mod_config)
        env.set_persist_provider(self.provider)

    def tear_down(self, success, exception=None):
        self.provider.persist_strategy(self._mod_config)

    def close(self):
        self.provider.close()