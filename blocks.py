from random import random


class Block:

    list_of_blocks_height = []
    id = 1

    def __init__(self, miner, father, BLOCK_REWARD, fee=0):
        """
        This class is for block!
        :param miner: id's miner's block
        :param father: id's block that current block mines on it.
        :param BLOCK_REWARD: reward of mining block
        :param fee: a random number.
        """
        self.id = Block.id
        self.miner_id = miner
        self.father = father
        self.block_height = self.father + 1
        self.block_reward = BLOCK_REWARD
        self.fee = fee
        Block.id += 1

    def __str__(self):
        return self.__dict__

    def add_block_height(self, fee=None):
        """
        if block height for new block does not exist in list of blocks height add it.
        :return:
        """
        if self.block_height not in Block.list_of_blocks_height:
            Block.list_of_blocks_height.append(self.block_height)


class Chain:
    """
    a list of object such that each object is a chain with key is id block that fork start it,
    """
    chains = []

    def __init__(self, id_block_new_chain, chain):
        self.chain_id = id_block_new_chain
        self.chain=chain
        Chain.chains.append(self)


