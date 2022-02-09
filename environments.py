import json
import random
from constant import LIMIT_FEE


class Environment:

    def __init__(self, n, number_block, number_agent, e, hash_mining_pool=None):
        """
        :param n: step of simulation
        :param number_block: number of blocks
        :param number_agent: number of agents
        :param e: ??
        """
        self.n = n
        self.number_block = number_block
        self.number_agent = number_agent
        self.main_matrix_block = []
        self.e = e
        self.fee = []

    def add_fee(self):
        r = random.randint(1, LIMIT_FEE)
        self.fee.append(r)
        return r

    def write_file(self, path):
        with open(path,'a') as env:
            json.dump(self.__dict__, env)

    def createMatrixForPolicy(self):
        """
        This function create new fee for new block before mine.
        :return:
        """
        fee = self.add_fee()
        list_len_row = []
        main_matrix_block_tempt=tuple(self.main_matrix_block)
        main_matrix_block_tempt=list(main_matrix_block_tempt)
        if self.main_matrix_block:
            for row in self.main_matrix_block:
                len_row = len(row)
                list_len_row.append(len_row)
            max_row = max(list_len_row)
            index=list_len_row.index(max_row)
            main_matrix_block_tempt[index].append((0, 0, fee))
        else:
            main_matrix_block_tempt.append([(0, 0, fee)])
        return main_matrix_block_tempt, fee
