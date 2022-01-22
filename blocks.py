from agents import Agents
import numpy as np
import random
from constant import BLOCK_REWARD, LIMIT_HASH_POWER, LIMIT_LENGTH_CHAIN


def multiply(matrix, i):
    """
    :param matrix: hash_power matrix for DDos
    :param i: i agent
    :return:multiply the i th column
    """
    matrix = np.array(matrix)
    n = len(matrix)
    vec = matrix[:, i]
    s = 1
    for j in range(n):
        s = s * (1 - vec[j])
    return s


def find_owner(lst: list, r):
    """
    determine owner of block
    :param lst:list of agent and The amount of hash power they put on this block!list of tuple.
    :param r: random number.
    :return:owner of block
    """
    lst.insert(0, (0, 0))
    lst.append((0, 0))
    for i in range(len(lst) - 1):
        if lst[i][1] <= r <= lst[i + 1][1]:
            return i + 1


class Block:
    id = 0
    list_of_blocks_height = []

    def __init__(self, owner, father, status=False, visibility=None):
        """
        :param id: this is a unique id and we don't have block with 0.
        :param owner: id of agent that mined block.
        :param father: id if block that new block mined on ir.
        :param status: ???
        :param visibility:???
        :param block_height: block_father +1 ??????
        """
        self.id = Block.id + 1
        self.owner = owner
        self.father = father
        self.block_height = self.father + 1
        self.block_reward = BLOCK_REWARD
        self.status = status
        self.visibility = visibility
        Block.id += 1

    def __str__(self):
        return f"owner:{self.owner}"

    def addBlockHeight(self, fee=None):
        """
        if block height for new block does not exist in list of blocks height add it.
        :return:
        """
        if self.block_height not in Block.list_of_blocks_height:
            Block.list_of_blocks_height.append(self.block_height)

    @staticmethod
    def payoff(e):
        """
        step 1: for all users we call policy and specify the amount of hash
        that has been attacked by other agents.
        step 2: calculate effective hash for each agent by action method in Agent class.
        :param e:???
        :return: list of effective hash for agents.(pay_off)
        """
        pay_off = {}
        matrix = []
        users = Agents.agents
        for i in users:
            context = i.strategy
            matrix.append(context)
        SUM = 0
        for i in users:
            s = multiply(matrix, i.id - 1)
            sT = i.action(e, matrix[i.id - 1]) * s
            i.effective_hash = sT
            pay_off[i.id] = sT
        return pay_off

    @staticmethod
    def mining(payoff, n=None):
        """
        This function determine status of each block
        :param payoff: {'user_id': hash_power, ... }
        :param n: number of before block for determine chain
        :return: block mines or not and if block mine which agent mines it.
        """
        r = random.randint(1, LIMIT_HASH_POWER)
        sumH = sum(list(payoff.values()))
        payoff = sorted(payoff.items(), key=lambda item: item[1])
        ro = random.randint(1, sumH)
        if r < sumH:
            own = find_owner(payoff, ro)
            block = Block(owner=own)
            return block
        else:
            return None

    def createVisibilityBlockForEachAgent(self):
        """
        for each new block determine for which agents is visible.
        :return:
        """
        id = Agents.agents.index(self.owner)
        agent = Agents.agents[id]
        visibility = agent.agent_visible
        for i in range(len(visibility)):
            if visibility[i] != 0:
                agent = Agents.agents[i + 1]
                agent.block_id_visible.append(self.id)


class Chain:
    """
    a matrix of tuples (id_owner,id_block)
    The number of rows in the matrix determines the number of forks.
    The first line represents the canonical chain.
    """
    chains = []

    def __init__(self, id_agent, id_block, id_block_father):
        """
        :param id_agent: id miner of block
        :param id_block: id of block
        :param id_block_father: id of block's father

        """
        self.block = (id_agent, id_block)
        self.father = id_block_father

    def determineChainOfBlock(self):
        """
        This function specifies which chain this block belongs to and then adds to it.
        :return: id_chain=(row,column)
        """
        id_chain = [(k, i) for k in range(len(Chain.chains)) for i, v in
                    enumerate(Chain.chains[k]) if v[1] == self.father]
        return id_chain[0]

    def addNewBlockToChain(self, place: tuple):
        """
        :param place: tuple of row number and father block number
        :return: updated chains matrix
        """
        columns = len(Chain.chains[place[0]])
        if columns == place[1] + 1:
            # we don't have fork.and block append end of chain.
            Chain.chains[place[0]].append(self.block)
        else:
            # fork.and create new chain.
            n = place[1] + 1
            chain = [(0, 0)] * n
            chain[place[1]] = self.block
            Chain.chains.append(chain)
        return Chain.chains

    @classmethod
    def lowLength(cls):
        """
        step 1: calculate number of blocks in each chains. we know (0,0) is not a block
        and first row is canonical chain.
        step 2 : compare every both chains in chains matrix.
        Add a chain index whose length is at least one chain less than LIMIT_LENGTH_CHAIN to
        the remove_chain.
        step 3 : Delete chains that in remove_chain from chains matrix .
        :return:updated chains matrix after low length
        """
        len_of_each_rows = []
        remove_chain = []

        for i in range(len(Chain.chains)):
            row = [j for j in cls.chains[i] if j != (0, 0)]
            len_of_each_rows.append(len(row))
        for i in range(1, len(len_of_each_rows) - 1):
            for j in range(i + 1, len(len_of_each_rows)):
                if len_of_each_rows[i] - len_of_each_rows[j] >= LIMIT_LENGTH_CHAIN:
                    remove_chain.append(j)
                elif len_of_each_rows[i] - len_of_each_rows[j] <= -1 * LIMIT_LENGTH_CHAIN:
                    remove_chain.append(i)
        remove_chain.sort(reverse=True)
        for k in remove_chain:
            cls.chains.pop(k)

        return Chain.chains

    @classmethod
    def lowSameFirstBlockAndAddToCanonicalChain(cls):
        """
        step 1: remove (0,0) from each chains of chains matrix.
        step 2: compare The first member of all the chains and if it's same we add it to
        canonical chain that is first row of chains matrix.
        :return:updated chains matrix .
        """
        list_of_chains = []
        for i in range(len(cls.chains)):
            row = [j for j in cls.chains[i] if j != (0, 0)]
            list_of_chains.append(row)

        for i in range(1, len(list_of_chains) - 1):
            if list_of_chains[i][0] != list_of_chains[i + 1][0]:
                break
        else:
            cls.chains[0].append(list_of_chains[i][0])
        return cls.chains


"""
یه کلاس chain داشته باشیم که لیستی از آرایه هاست و اگه طولش 1 باشه که هیچی اگه طولش بیشتر 
از یک باشه یعنی فورک داریم و برای هر فورکی باز یه ارایه داریم که بلاک های هرکدومش توش باشه.
دو قانون برای هر زنجیر داریم اول اینکه طول هر زنجیری که طولش  n تااز بقیه کمتر باشه رو حذف میکنیم
و اینکه و چک میکنیم اگه بلاک اول همه مشترک بود به بلاک فاینال تو محیط اضاف میشه :)
یه visibility داریم که بعد از اینکه هر بلاکی ماین شد به ماینر نشون میده که بگه میخوای به کیا نشونش بدی. 
"""
