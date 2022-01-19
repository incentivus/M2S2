from simlation import getDataFromDatabase, createObjectAgentAndAddPolicy, createEnvironment
from constant import *

AGENTS = getDataFromDatabase()
NUMBER_OF_AGENTS = len(AGENTS)
createObjectAgentAndAddPolicy(AGENTS, PATH)
createEnvironment(number_of_round_game=NUMBER_OF_ROUND_GAME, number_of_agents=NUMBER_OF_AGENTS,
                  number_of_blocks=NUMBER_OF_BLOCK_FOR_EACH_ROUND, agents=AGENTS, path='environment')
