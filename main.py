from enviromnment import *

# Initial input
agents_no = 2
blocks_no = 1000
Hash = 100
simulations_no = 10
reward = 10

# determine kind of agents
agents_type = {
    'selfish': 1,
}

# start game Honest


# env = Env(number_blocks=blocks_no, number_agents=agents_no, block_reward=reward, hash=Hash)
# genesis_block = Block(miner=0 , father=0 , BLOCK_REWARD=reward)
# env.create_chain(genesis_block)
# lst_hash = env.decomposition()
# env.create_lst_agents_hash()
# env.create_agents_honest(lst_hash)
# for w in range(env.number_blocks):
#     blocks, miners = env.determine_block_honest()
#     blocks=list(set(blocks))
#     block = env.mining(blocks=blocks, id_agent_block_mine=miners)
#     if block:
#         env.create_chain(block)
#     else:
#         w = w - 1


# start game Selfish
env = Env(number_blocks=blocks_no, number_agents=agents_no, block_reward=reward, hash=Hash)
genesis_block = Block(miner=0 , father=0 , BLOCK_REWARD=reward)
env.create_chain(genesis_block)
alpha = 0.1
for al in range(10 , 60 ,10):
    selfish=Agent(hash_power=al,blockchain=env.obj_blocks,typ="selfish")
    honest = Agent(hash_power=Hash - al ,blockchain=env.obj_blocks,typ="honest")
    env.obj_agents.append(selfish)
    env.obj_agents.append(honest)
    for w in range(env.number_blocks):
        blocks, miners = env.determine_block_honest()
        blocks = list(set(blocks))
        block = env.mining(blocks=blocks, id_agent_block_mine=miners)
        if block:
            env.create_chain(block)
        else:
            w = w - 1