**Usage**
=========

.. _installation:

**Installation**
----------------

To use our simulator, first install it using pip:

.. code-block:: console
	
	(.venv) $ pip install Blockchain-Simulator


**Policy function**
--------------------

Each ``policy()`` function has three input values, respectively, the hash-power of the miner,
the blocks-visible (local blockchain) and the hash-power of other miners, which is given to
the function in a list.

.. py:function:: policy(hash_power, block_visible, agents_hash)

	Return a dictionary with keys blocks, strategy and visibility.
	
	:param hash_power: Hash power of miner that determine randomly.
	:type hash_power: int
	:param blocks_visible: Blocks that are visible to miner. (local blockchain)
	:type hash_power: list[typle]
	:param agents_hash: hash power of other miners.
	:type hash_power: list[int]
	:return: Dictionary with keys blocks,strategy,visiblity.

**Main input parameters**
--------------------------

At the beginning of the simulation, you can determine the parameters related to the number of blocks and the number of agents and the amount of block mining reward.
The following table shows the main input parameters to start the simulation process.


+--------------+--------------------------------------------------------------------+
| Parameters   |                         Discription                                |
+==============+====================================================================+
| N_AGENTS     | Determine the total number of nodes in the simulation              |
+--------------+--------------------------------------------------------------------+
| N_BLOCKS     | Determine the total number of blocks in the simulation             |
+--------------+--------------------------------------------------------------------+
| HASH         | Determine the total hash power of system                           |
+--------------+--------------------------------------------------------------------+
| NUM_TYPE     | Determine the types of miners and their percentage in the system   |
+--------------+--------------------------------------------------------------------+
| BLOCK_REWARD | Determine reward of block mined                                    |
+--------------+--------------------------------------------------------------------+


	

