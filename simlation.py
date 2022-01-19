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
    Users = []
    return Users


def createObjectAgentAndAddPolicy(users, path):
    """
    for each user create Agent object.
    :param users: list of users and path of policy's file.
    :param path: path of folder includes files of policies.
    :return:
    """
    for i in users:
        agent = Agents(user_name=i['name'])
        with open(f"{path}/{i['path']}") as file:
            func = file.read()
            exec(func)
            agent.policy = POLICY


def createRandomHashPower(limit_hash_power):
    """
    this function create a random hash_power for each agent.
    :param limit_hash_power: maximum of hash power can get.
    :return:
    """
    for u in Agents.agents:
        HASH = randint(1, limit_hash_power)
        u.hash_power = HASH


def policyAndCheck(agents, fee):
    """
    this function call policy and check output is correct.
    :param agents: list of all object agents.
    :return:
    """
    for i in agents:
        i.callPolicy(fee)
        i.checkOutputPolicy()


def callVisibleMatrixForEachUser(agents, main_matrix, new_block):
    for i in agents:
        i.createMatrixVisible(main_matrix, new_block)


def createEnvironment(number_of_round_game, number_of_agents, number_of_blocks, limit_hash_power, agents,path):
    for i in range(number_of_round_game):
        env = Environment(n=i, number_agent=number_of_agents, number_block=number_of_blocks,
                          e=random())
        main_matrix, fee = env.main_matrix_block()

        createRandomHashPower(limit_hash_power)
        policyAndCheck(agents, fee)
        matrix_for_mine = Agents.createMatrixOfBlocksAgentsWantsToMine()
        rows = len(matrix_for_mine)
        columns = len(matrix_for_mine[0])
        for k in columns:
            pay_off = Block.payoff(env.e)
            block = Block.mining(pay_off)
            if block is not None:
                block.addBlockHeight()
                block.createVisibilityBlockForEachAgent()
                block_in_chain = Chain(block.id, block.owner, block.father)
                place = block_in_chain.determineChainOfBlock()
                block_in_chain.addNewBlockToChain(place)
                Chain.lowLength()
                Chain.lowSameFirstBlockAndAddToCanonicalChain()
                env.main_matrix_block = Chain.chains
                new_block_id = (block.id, block.owner, fee)
                callVisibleMatrixForEachUser(env.main_matrix_block,new_block_id)
        env.write_file(path)