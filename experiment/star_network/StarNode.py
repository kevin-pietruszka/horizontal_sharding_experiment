from queue import Queue
from threading import Thread
from util.table import Table
import pandas as pd
from collections.abc import Sequence
from util.errors import NoConnections
from network_transfer.Bandwidth import Bandwidth
from my_statistics.StatisticsTable import StatisticsTable

class StarNode:
    
    def __init__(self, id:int, df:pd.DataFrame, transfer_speed: float = 1) -> None:
        self.table = Table(df)
        self.id = id
        self.connections = None
        self.connection = Bandwidth(transfer_speed)
        self.stats = StatisticsTable()
    
    def set_connections(self, others: Sequence['StarNode']):
        self.connections = others

    def query(self, column: str, predicate: str, value: int) -> pd.DataFrame:
        """Execute query on all nodes and return result"""
        if self.connections == None:
            raise NoConnections

        connection_outputs = Queue()
        for connection in self.connections:
            x = Thread(target=connection._query, args=(connection_outputs, column, predicate, value))
            x.start()

        # Execute Query on this device
        output_df = self.table.query(column, predicate, value)
        self.stats.update(output_df)

        # Combine output
        for i in range(len(self.connections)):
            res = connection_outputs.get()
            output_df = pd.concat([output_df, res])

        return output_df

    def _query(self, output_queue: Queue, column: str, predicate: str, value: int):
        my_output = self.table.query(column, predicate, value)
        self.connection.send_df(my_output)
        output_queue.put(my_output)
