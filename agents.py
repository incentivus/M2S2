import numpy as np


# chains = {'canonical': {}, 'forks': {1: {}, 2: {}}}


class Agents:
    agents = []
    agents_dic = []
    id = 1

    def __init__(self, user_name, hash_power=0, hash_effective=None):
        """
        :param id : this id a unique id and we don't have agent with id 0.
        :param user_name: email address for each user.
        :param hash_power : a random number.
        :param hash_effective: hash after attack!
        :param block_id_visible: id of blocks that agent can see them.
        :param matrix_visible : a matrix of chains that agent can see them.
                each block is triple of block_id ,agent_id and fee.
        :param strategy : a list of can determine agent attack to which agents.
        :param block_for_mine: a list of block and hash of block that agent want to mine them.
        :param agent_visible : a list binary of agent suck that if block is mine witch agent can
                see it.
        """
        self.id = Agents.id
        self.user_name = user_name
        self.hash_power = hash_power
        self.hash_effective = hash_effective
        self.block_id_visible = []
        self.matrix_visible = []
        self.strategy = []
        self.blocks_for_mine = []
        self.agent_visible = []
        Agents.agents.append(self)
        Agents.agents_dic.append(self.__dict__)
        Agents.id += 1

    def createMatrixVisible(self, main_block_matrix, new_block_id):
        """
        create matrix of block.
        if chain of new block exist , add block end of it, else we add chain to matrix.
        :param main_block_matrix: Every element is a list af triple block_id,owner_id and fee.
        :param new_block_id: a triple (block_id,owner_id,fee) for new block is mine.
        :return: updated matrix_visible.
        """
        if new_block_id in self.block_id_visible:
            for ch in main_block_matrix:
                if new_block_id in ch:
                    row = [j for j in ch if j != new_block_id]
                    if row not in self.matrix_visible:
                        self.matrix_visible.append(ch)
                        return self.matrix_visible
                    else:
                        index = self.matrix_visible.index(row)
                        self.matrix_visible[index].append(new_block_id)
                        return self.matrix_visible

        else:
            return self.matrix_visible

    def createMatrixForPolicy(self, fee):
        """
        this function create matrix for policy
        :return: a matrix of block can see with fee and fee of new block.
        """
        matrix_visible_temp = self.matrix_visible
        list_len_row = []
        if matrix_visible_temp:
            for row in self.matrix_visible:
                len_row = len(row)
                list_len_row.append(len_row)
            max_row = max(list_len_row)
            index=list_len_row.index(max_row)
            matrix_visible_temp[index].append((0, 0, fee))
        else:
            matrix_visible_temp.append([(0, 0, fee)])
        return matrix_visible_temp, fee

    def policy(self,hash_power,matrix,agent_hash):
        """
        This function writes by students!POLICY
        [{1:10,2:20}]
        :return: {'block':[hash for each block that they can mine it this is a
         dictionary of id block father and amount of hash],'strategy':[honest or DDos],
        'visibility':[if block is mined which agents can see it]}
        """
        pass

    def action(self, e, *args):
        """This function for DDos attack!"""
        args = np.array(args)
        sTilda = (1 + e * (1 - np.sum(args))) * self.hash_power
        return sTilda

    def callPolicy(self, fee,agent_hash):
        """
        for each agent call policy and return vector of block
        """
        matrix_visible_temp,fee = self.createMatrixForPolicy(fee)
        context = self.policy(self.hash_power, matrix_visible_temp,agent_hash)
        self.blocks_for_mine = context['block']  ### همین جا باید کدوم بلاک چقدره رو جدا کنی!!!
        self.strategy = context['strategy']
        self.agent_visible = context['visibility']

    def checkOutputPolicy(self):
        """
        check sum of hash for each strategy and block be hash power.
        :return:
        """
        sum_strategy = sum(self.strategy)
        block=[]
        for i in self.blocks_for_mine:
            key=list(i.keys())[0]
            block.append(i[key])
        sum_block = sum(block)
        if sum_block + sum_strategy != self.hash_power:
            self.strategy = 0
            self.blocks_for_mine = 0

    def hashOfEachBlockAfterAttack(self):
        """
        :return: a dictionary of block_id : hash after attack
        """
        hash_block = self.blocks_for_mine
        attack = self.hash_power - self.hash_effective
        for i in hash_block:
            name=list(i.keys())[0]
            j = i[name] - attack
            i[name]=j
        return hash_block

    def blocksAgentWantToMine(self):
        """
        Determine which blocks are wanted to mine!
        :return:list of id of blocks
        """
        block_and_hash = self.hashOfEachBlockAfterAttack()
        blocks=[]
        for i in block_and_hash:
            name=list(i.keys())[0]
            blocks.append(name)
        return blocks

    def __str__(self):
        return self.user_name, self.hash_power

    @staticmethod
    def createMatrixOfBlocksAgentsWantsToMine():
        """
        step 1: determine which blocks may be mine!
        :return: a matrix !
        """
        agents = Agents.agents
        matrix = [0] * len(agents)
        set_block = []
        agent_block = []
        for i in agents:
            v = {}
            b = i.blocksAgentWantToMine()
            for j in b:
                set_block.append(j)
            v[i.id] = b
            agent_block.append(v)
        set_block.sort()
        set_block = set(set_block)
        len_blocks=len(set_block)
        for i in range(len(matrix)):
            matrix[i]=[0]*len_blocks
        k = 0
        for i in agents:
            for j in set_block:
                if j in agent_block[k][i.id]:
                    hash_block=i.hashOfEachBlockAfterAttack()
                    keys=[]
                    for q in hash_block:
                        key=list(q.keys())[0]
                        keys.append(key)
                    index=keys.index(j)
                    matrix[i.id-1][j-1] = hash_block[index][j]
                else:
                    matrix[i.id][j] = 0
                k += 1
        return matrix ,list(set_block)
