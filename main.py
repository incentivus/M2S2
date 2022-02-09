from simulation import getDataFromDatabase, createEnvironment
from constant import *
import agents
AGENTS = getDataFromDatabase()
for i in AGENTS:
    agent=agents.Agents(user_name=i)
    with open(f"policies/{i}.txt") as file:
        func = file.read()
        exec(func)
        agent.policy = POLICY
NUMBER_OF_AGENTS = len(AGENTS)
createEnvironment(number_of_round_game=NUMBER_OF_ROUND_GAME, number_of_agents=NUMBER_OF_AGENTS,
                  number_of_blocks=NUMBER_OF_BLOCK_FOR_EACH_ROUND, agents=AGENTS, path='environment',
                limit_hash_power=LIMIT_HASH_POWER)
