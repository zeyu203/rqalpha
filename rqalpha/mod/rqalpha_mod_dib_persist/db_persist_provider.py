import time
import pymongo

from rqalpha.interface import AbstractPersistProvider


class DBPersistProvider(AbstractPersistProvider):
    parent_strategy_id = 0
    strategy_id = 0
    db = None
    client = None

    def __init__(self, config):
        self.parent_strategy_id = config.base.parent_id
        host = config.mongo.host
        port = config.mongo.port

        self.client = pymongo.MongoClient(host=host, port=port)
        self.db = self.client.dibquant

        if self.db['strategy_ids'].find_one({'name': 'user'}) is None:
            self.db['strategy_ids'].save({'name' : 'user', 'id' : 0})

        result = self.db['strategy_ids'].find_and_modify(
            query={'name': 'user'},
            fields={'id': 1, '_id': 0},
            update={'$inc': {'id' : 1}},
            new=True)

        self.strategy_id = result['id']

    def store(self, key, value):
        assert isinstance(value, bytes), "value must be bytes"
        data = {'strategy_id' : self.strategy_id, 'value' : value}
        self.db[key].update({"strategy_id" : self.strategy_id}, data, True)

    def load(self, key, strategy_id = 0):
        if strategy_id <= 0:
            strategy_id = self.strategy_id
        data = self.db[key].find_one({"strategy_id" : strategy_id})
        return data['value'] if data is not None and 'value' in data else None

    def persist_strategy(self, config):
        data = {
            'strategy_id' : self.strategy_id,
            'parent_strategy_id' : self.parent_strategy_id,
            'benchmark' : config.base.benchmark,
            'start_date' : config.base.start_date.strftime("%Y-%m-%d"),
            'end_date' : config.base.end_date.strftime("%Y-%m-%d"),
            'frequency' : config.base.frequency,
            'market' : config.base.market.value,
            'run_type' : config.base.run_type.value,
            'strategy_file' : config.base.strategy_file,
            'run_time' : config.run_time,
            'modify_time' : time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        }
        self.db['strategy'].update({'strategy_id' : self.strategy_id}, data, True)

    def close(self):
        self.client.close()