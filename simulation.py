from agents import Agents
from environments import Environment
from random import random, randint
from blocks import Block, Chain


def getDataFromDatabase():
    """
    This function connect to postgres and get data.
     first it save policy in txt file in policies folder.
     then append name of the file to value of user's dictionary.
    :return: a list of users and path of policy file. [{'name':'path'}]
    """
    Users = ['fateme', 'mona', 'faeze']

    return Users


def createRandomHashPower(limit_hash_power):
    """
    this function create a random hash_power for each agent.
    :param limit_hash_power: maximum of hash power can get.
    :return:
    """
    agent_hash = []
    for u in Agents.agents:
        HASH = randint(1, limit_hash_power)
        if HASH in agent_hash:
            continue
        else:
            u.hash_power = HASH
            agent_hash.append(HASH)
    return agent_hash


def policyAndCheck(agents, fee, agent_hash):
    """
    this function call policy and check output is correct.
    :param agents: list of all object agents.
    :return:
    """
    for i in agents:
        i.callPolicy(fee, agent_hash)
        i.checkOutputPolicy()


def callVisibleMatrixForEachUser(agents, main_matrix, new_block):
    for i in agents:
        i.createMatrixVisible(main_matrix, new_block)


def createEnvironment(number_of_round_game, number_of_agents, number_of_blocks, limit_hash_power, agents, path):
    agent_hash = createRandomHashPower(limit_hash_power)
    for i in range(number_of_round_game):
        env = Environment(n=i, number_agent=number_of_agents, number_block=number_of_blocks,
                          e=random())
        number = 0
        while number < number_of_blocks:
            main_matrix, fee = env.createMatrixForPolicy()
            print(env.main_matrix_block)
            policyAndCheck(Agents.agents, fee, agent_hash)
            pay_off = Block.payoff(env.e)
            matrix_for_mine ,set_block = Agents.createMatrixOfBlocksAgentsWantsToMine()
            rows = len(matrix_for_mine)
            columns = len(matrix_for_mine[0])
            for k in range(columns):
                block = Block.mining(pay_off, set_block[k],fee)
                if block is not None:
                    block.addBlockHeight()
                    block.createVisibilityBlockForEachAgent()
                    block_in_chain = Chain(block.owner, block.id, block.father,block.fee)
                    block_in_chain.createChains()
                    place = block_in_chain.determineChainOfBlock()
                    block_in_chain.addNewBlockToChain(place)
                    Chain.lowLength()
                    Chain.lowSameFirstBlockAndAddToCanonicalChain()
                    env.main_matrix_block = Chain.chains
                    #env.main_matrix_block=list(env.main_matrix_block)
                    new_block_id = (block.id, block.owner, fee)
                    callVisibleMatrixForEachUser(Agents.agents,env.main_matrix_block, new_block_id)
                    number += 1
                else:
                    for chain in main_matrix:
                        if (0, 0, fee) in chain:
                            chain.pop()
        pathh=f"{path}/{i}.txt"
        env.write_file(pathh)
