from random import random, randint, sample
import numpy as np
from agents import Agent
from blocks import Block, Chain


class Env:

    def __init__(self, number_blocks, number_agents, block_reward, hash):
        self.number_blocks = number_blocks
        self.number_agents = number_agents
        self.block_reward = block_reward
        self.hash = hash
        self.lst_hash_agent = []
        self.obj_agents = []
        self.obj_blocks = []
        self.obj_blocks_all = []
        self.agents_selfish = []

    def decomposition(self):
        hash = self.hash - 1
        lst = []

        lst_b = sample(range(1, hash), self.number_agents - 1)
        lst_b.sort()

        lst_b.append(0)
        lst_b.append(hash + 1)
        lst_b.sort()

        for i in range(len(lst_b) - 1):
            lst.append(lst_b[i + 1] - lst_b[i] - 1)
        return lst

    def create_agents_selfish(self, numbers_of_type, lst_hash):
        for k in numbers_of_type:
            if k == "selfish":
                hsh = max(lst_hash)
                for i in self.obj_agents:
                    if i.hash_power == hsh:
                        i.typ = "selfish"
                        self.agents_selfish.append(i)
            elif k == "DDoss":
                num = int(self.number_agents * numbers_of_type[k] / 100)
                print(num)
                hash_less_10 = []
                h = 10 * self.hash / 100
                for i in range(len(self.lst_hash_agent)):
                    if self.lst_hash_agent[i] < h:
                        hash_less_10.append(i)
                if len(hash_less_10) == num:
                    for j in self.obj_agents:
                        for l in hash_less_10:
                            if j.id == l + 1:
                                j.typ = "10DDoss"
                elif len(hash_less_10) > num:
                    hash_less_10 = hash_less_10[0:num]
                    for j in self.obj_agents:
                        for l in hash_less_10:
                            if j.id == l + 1:
                                j.typ = "10DDoss"
                elif len(hash_less_10) < num:
                    t = 0
                    for j in self.obj_agents:
                        for l in hash_less_10:
                            if j.id == l + 1:
                                j.typ = "10DDoss"
                    for j in self.obj_agents:
                        if t < num - len(hash_less_10):
                            if j.typ == "honest":
                                if j.id % 2 == 0:
                                    j.typ = "DDoss"
                                    t += 1
                                else:
                                    j.typ = "4DDoss"
                                    t += 1

            # self.agent_ddoss=[Agent(hash_power=hsh,typ=k) for hsh in ]

    def create_agents_honest(self, lst_hash):
        self.obj_agents = [Agent(hash_power=h, typ="honest", blockchain=self.obj_blocks) for h in lst_hash]

    def create_lst_agents_hash(self):
        lst = [0] * self.number_agents
        for i in self.obj_agents:
            lst[i.id - 1] = i.hash_power
        self.lst_hash_agent = lst

    def determine_block_for_mine(self):
        blocks = []
        ids_selfish = []
        ids_agents_mine_block = []
        for i in self.obj_agents:
            if i.typ == "DDoss":
                context = i.policy_ddoss(self.lst_hash_agent)
                i.block = context['block']
                i.strategy = context['strategy']

            elif i.typ == "4DDoss":
                context = i.policy_4ddoss(self.lst_hash_agent)
                i.block = context['block']
                i.strategy = context['strategy']

            elif i.typ == "10DDoss":
                context = i.policy_10ddoss(self.lst_hash_agent)
                i.block = context['block']
                i.strategy = context['strategy']

            elif i.typ == "selfish":
                context = i.policy_selfish(self.lst_hash_agent)
                i.block = context['block']
                i.strategy = context['strategy']
                i.visible = context['visibility']
                blocks.append(i.block[0])
                ids_agents_mine_block.append((i.id, i.block[0], i.block[1]))
                if 0 in i.visible:
                    ids_selfish.append(i.id)

            elif i.typ == "honest":
                context = i.policy_honest(self.lst_hash_agent)
                i.block = context['block']
                i.strategy = context['strategy']
                blocks.append(i.block[0])
                ids_agents_mine_block.append((i.id, i.block[0], i.block[1]))
        return blocks, ids_agents_mine_block

    def determine_block_honest(self):
        blocks = []
        id_agents_mine = []
        for i in self.obj_agents:
            context = i.policy_honest(self.lst_hash_agent)
            i.block = context['block']
            blocks.append(i.block[0])
            id_agents_mine.append((i.id, i.block[0], i.block[1]))
        return blocks, id_agents_mine

    def hash_effective(self, e):
        hash_efc = 0
        mat = [0] * self.number_agents
        for i in self.obj_agents:
            t = np.array(i.strategy)
            mat[i.id - 1] = t / i.hash_power

        matt = np.matrix(mat)
        sum_matt = matt.sum(axis=1)
        mul_matt = [0] * self.number_agents
        for i in range(self.number_agents):
            v = 1
            for j in range(self.number_agents):
                v = (1 - mat[j][i]) * v
            # print(v)
            mul_matt[i] = v

        for i in self.obj_agents:
            i.hash_effective = int((1 + e) * (i.hash_power) * (1 - sum_matt[i.id - 1]) * (mul_matt[i.id - 1]))
            if i.hash_effective < 0:
                i.hash_effective = 0

    def mining(self, blocks, id_agent_block_mine):
        for i in blocks:
            pay_off = [0] * self.number_agents
            for j in id_agent_block_mine:
                if j[1] == i:
                    pay_off[j[0] - 1] = j[2]
            r = randint(1, self.hash)
            sumH = sum(pay_off)
            pay_off = enumerate(pay_off)
            sort_pay_off = sorted(pay_off, key=lambda x: x[1])
            if r < sumH:
                for k in sort_pay_off:
                    if r < k[1]:
                        miner = k[0] + 1
                        b = Block(miner=miner, father=i, BLOCK_REWARD=self.block_reward)
                        b.add_block_height()
                        return b
            else:
                return False

    def hash_block_ddoss(self, id_agents_mine):
        id_agents = []
        for i in self.obj_agents:
            for j in id_agents_mine:
                if j[0] == i.id:
                    h = (j[0], j[1], i.hash_effective)
                    id_agents.append(h)
        return id_agents

    def create_chain(self, b, new=False):
        if new:
            for i in self.obj_blocks_all:
                if b.father == i[-1].id:
                    i.append(b)
            else:
                self.obj_blocks_all.append([b])
                Chain(id_block_new_chain=b.father, chain=b)
        else:
            for i in self.obj_blocks:
                if b.father == i[-1].id:
                    i.append(b)
            else:
                self.obj_blocks.append([b])
                self.obj_blocks_all.append([b])
                Chain(id_block_new_chain=b.father, chain=b)

    def low_length(self):
        ch = Chain.chains
        remove = []
        for i in range(len(ch)):
            for j in range(len(ch)):
                if len(i) - len(j) > 6:
                    remove.append(ch(j))
        ch = ch - remove
        self.obj_blocks = ch

    def add_canonical(self):
        pass
