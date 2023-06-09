
import numpy as np
import pandas as pd
from star_network.StarNode import StarNode
from sharding_methods.EvenSplit import even_split
import random
from my_statistics.StatisticsTable import StatisticsTable

NUM_SERVERS = 5

def main():
    
    ids = np.array(range(1,11))
    ratings = np.random.rand(10)
    ratings = np.multiply(ratings, 10)

    df = pd.DataFrame()
    df["id"] = ids
    df["rating"] = ratings

    frames = even_split(df,NUM_SERVERS)
    
    nodes = []
    for i in range(NUM_SERVERS):
        new_node = StarNode(i, frames[i])
        nodes.append(new_node)

    for i in range(len(nodes)):
        others = nodes[:i] + nodes[i+1:]
        nodes[i].set_connections(others)

    chosen_node = random.randint(0, NUM_SERVERS - 1)

    # query_output = nodes[chosen_node].query('rating', 'GT', 0)
    # print(query_output)

    stats = []
    for i in range(len(nodes)):
        nodes[i].query('rating', 'GT', 0)
        stats.append(nodes[i].stats)
        # print(nodes[i].stats.counts)

    nd_arr = StatisticsTable.combine(len(df), stats)
    print(nd_arr)

if __name__ == "__main__":
    main()