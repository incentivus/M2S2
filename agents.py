import numpy as np


class Agent:
    id = 1

    def __init__(self, hash_power, blockchain, typ='honest'):
        """

        :param hash_power: hash power of miner
        :param blockchain: local blockchain
        :param typ: Specify miner of block.
        """
        self.id = Agent.id
        self.hash_power = hash_power
        self.typ = typ
        self.blockchain = blockchain
        self.hash_effective = hash_power
        self.strategy = []
        self.blocks = []
        Agent.id += 1

    def policy_honest(self, agents_hash):
        n = len(agents_hash)
        strategy = n * [0]
        visibility = n * [1]
        max_len = 0
        longest_chain = 0
        for i in range(len(self.blockchain)):
            if len(self.blockchain[i]) > max_len:
                max_len = len(self.blockchain[i])
                longest_chain = self.blockchain[i]

        block_id = longest_chain[-1].id
        valid_block_id = block_id

        block = (valid_block_id, self.hash_power)

        context = {'block': block, 'strategy': strategy, 'visibility': visibility}
        return context

    # DDoss for agent has the biggest hash power
    def policy_4ddoss(self, agents_hash):
        n = len(agents_hash)
        strategy = n * [0]
        visibility = n * [1]
        max_hash_power = max(agents_hash)
        max_id = agents_hash.index(max_hash_power)
        if max_id != self.id:
            strategy[max_id] = self.hash_power
        else:
            second_max = sorted(agents_hash, reverse=True)[1]
            third_max = sorted(agents_hash, reverse=True)[2]
            second_max_id = agents_hash.index(second_max)
            third_max_id = agents_hash.index(third_max)
            strategy[second_max_id] = self.hash_power / 2
            strategy[third_max_id] = self.hash_power / 2

        max_len = 0
        longest_chain = 0
        for i in range(len(self.blockchain)):
            if len(self.blockchain[i]) > max_len:
                max_len = len(self.blockchain[i])
                longest_chain = self.blockchain[i]

        block_id = longest_chain[-1].id
        valid_block_id = block_id

        block = (valid_block_id, 0)

        context = {'block': block, 'strategy': strategy, 'visibility': visibility}
        return context

    # if agent has less than 10% of hash_power of systems , he attacks to four agents have most hash power
    def policy_10ddoss(self, agents_hash):
        n = len(agents_hash)
        strategy = n * [0]
        visibility = n * [1]
        HASH = sum(agents_hash)

        max_len = 0
        longest_chain = 0
        for i in range(len(self.blockchain)):
            if len(self.blockchain[i]) > max_len:
                max_len = len(self.blockchain[i])
                longest_chain = self.blockchain[i]

        block_id = longest_chain[-1].id
        valid_block_id = block_id
        sorted_hash_power = sorted(agents_hash, reverse=True)
        values = np.array(sorted_hash_power)
        max_ids = np.where(values == sorted_hash_power[0])[0]
        if 1 < len(max_ids) <= 4:
            n = len(max_ids)
            for i in range(n):
                strategy[max_ids[i]] = self.hash_power / 4
        elif len(max_ids) > 4:
            for i in range(4):
                strategy[max_ids[i]] = self.hash_power / 4
        else:
            strategy[max_ids[0]] = self.hash_power / 4
        m = 4 - len(max_ids)
        ids = np.where(values == sorted_hash_power[1])[0]
        if 1 < len(ids) <= m:
            n = len(ids)
            for i in range(n):
                strategy[ids[i]] = self.hash_power / 4
        elif len(ids) > m:
            for i in range(m):
                strategy[ids[i]] = self.hash_power / 4
            else:
                strategy[ids[0]] = self.hash_power / 4
        m = m - len(ids)
        ids = np.where(values == sorted_hash_power[2])[0]
        if 1 < len(ids) <= m:
            n = len(ids)
            for i in range(n):
                strategy[ids[i]] = self.hash_power / 4
        elif len(ids) > m:
            for i in range(m):
                strategy[ids[i]] = self.hash_power / 4
            else:
                strategy[ids[0]] = self.hash_power / 4
        m = m - len(ids)
        ids = np.where(values == sorted_hash_power[3])[0]
        if 1 < len(ids) <= m:
            n = len(ids)
            for i in range(n):
                strategy[ids[i]] = self.hash_power / 4
        elif len(ids) > m:
            for i in range(m):
                strategy[ids[i]] = self.hash_power / 4
            else:
                strategy[ids[0]] = self.hash_power / 4

        block = (valid_block_id, 0)

        context = {'block': block, 'strategy': strategy, 'visibility': visibility}
        return context

    # Just DDoss
    def policy_ddoss(self, agents_hash):
        n = len(agents_hash)
        strategy = n * [0]
        visibility = n * [1]

        hash_attack = self.hash_power / (n - 1)
        for i in range(n):
            if i != self.id:
                strategy[i] = hash_attack
        max_len = 0
        longest_chain = 0
        for i in range(len(self.blockchain)):
            if len(self.blockchain[i]) > max_len:
                max_len = len(self.blockchain[i])
                longest_chain = self.blockchain[i]

        valid_block_id = 1
        for i in range(len(longest_chain)):
            block_id, owner_id, fee = longest_chain[-1 - i]
            if owner_id != 0:
                valid_block_id = block_id
                break

        block = (valid_block_id, 0)

        context = {'block': block, 'strategy': strategy, 'visibility': visibility}
        return context

    # if agent has more than 50% hash power of systems , he does selfish mining.
    def policy_selfish(self, agents_hash):
        n = len(agents_hash)
        strategy = n * [0]
        visibility = n * [1]
        max_len = 0
        longest_chain = 0
        for i in range(len(self.blockchain)):
            if len(self.blockchain[i]) > max_len:
                max_len = len(self.blockchain[i])
                longest_chain = self.blockchain[i]

        block_id = longest_chain[-1].id
        valid_block_id = block_id

        block = (valid_block_id, self.hash_power)
        context = {'block': block, 'strategy': strategy, 'visibility': visibility}
        return context
