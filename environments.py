import json
import random
from constant import LIMIT_FEE
from agents import Agents
from blocks import Block


class Environment:

    def __init__(self, n, number_block, number_agent, e, hash_mining_pool=None):
        """
        :param n: step of simulation
        :param number_block: number of blocks
        :param number_agent: number of agents
        :param hash_mining_pool: ??
        :param final_block: final block without fork and all agents can see them.
        :param e: ??
        """
        self.n = n
        self.number_block = number_block
        self.number_agent = number_agent
        self.hash_mining_pool = hash_mining_pool
        self.main_matrix_block = []
        self.e = e
        self.fee = []

    def add_fee(self):
        r = random.randint(1, LIMIT_FEE)
        self.fee.append(r)
        return r

    def write_file(self, path):
        with open(path, 'a') as env:
            json.dump(self.__dict__, env)

    def createMatrixForPolicy(self):
        """
        This function create new fee for new block before mine.
        :return:
        """
        fee = self.add_fee()
        list_len_row = []
        for row in self.main_matrix_block:
            len_row = len(row)
            list_len_row.append(len_row)
        max_row = max(list_len_row)
        self.main_matrix_block[max_row].append((0, 0, fee))
        return self.main_matrix_block , fee
