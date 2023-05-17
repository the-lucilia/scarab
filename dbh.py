import asyncio
import sqlite3
import threading
import uuid
from queue import Queue


class dbh:
    """
    Database handler wrapper.
    Provides a clean and easy to use interface for database operations.
    Passes all operations to a worker thread, which handles them in the background,
    allowing the main thread to continue without blocking.
    """

    def __init__(self):
        self.db = sqlite3.connect('scarab.db')
        self.db.row_factory = sqlite3.Row
        self.insert_queue = Queue()  # Queue of transactions to be inserted into the database (table, data, transaction_id)
        self.read_queue = Queue()  # Queue of transactions to be read from the database (table, keys, transaction_id)
        self.results_queue = Queue()  # Queue of results to be returned to the caller (transaction_id, results)
        self.work_stop = threading.Event()
        self.worker_thread = threading.Thread(target=self.worker)
        self.worker_thread.start()

    def worker(self):
        """
        Long-running worker thread that handles database operations.
        :return:
        """
        while True:
            if not threading.current_thread().is_alive():  # If the thread is dead, we die too
                break
            if self.work_stop.is_set():
                pass
            else:
                if not self.insert_queue.empty():
                    transaction = self.insert_queue.get()
                    table = transaction[0]
                    data = transaction[1]
                    transaction_id = transaction[2]
                    keys = [":" + key for key in data.keys()]
                    sql = f"INSERT INTO {table} (" + ", ".join(["?" for key in data.keys()]) + ") VALUES(" + ", ".join(
                        ["?" for key in data.keys()]) + ")"
                    cur = self.db.cursor()
                    cur.execute(sql, tuple(data.values()))
                    self.db.commit()
                    self.results_queue.put((transaction_id, cur.lastrowid))
                    self.insert_queue.task_done()

                elif not self.read_queue.empty():
                    transaction = self.read_queue.get()
                    table = transaction[0]
                    keys = transaction[1]
                    values = transaction[2]
                    transaction_id = transaction[3]
                    sql = f"SELECT * FROM {table} WHERE " + " AND ".join([f"{key} = ?" for key in keys])
                    cur = self.db.cursor()
                    cur.execute(sql, tuple(values))
                    rows = cur.fetchall()
                    self.results_queue.put((transaction_id, rows))
                    self.read_queue.task_done()

                else:
                    pass

    async def insert(self, table, data):
        """
        Insert a row into the database.
        :param table: Table to insert into
        :param data: Data to insert
        :return: Row ID of the inserted row
        """
        transaction_id = uuid.uuid4()
        self.insert_queue.put((table, data, transaction_id))
        while True:
            if not self.results_queue.empty():
                result = self.results_queue.get()
                if result[0] == transaction_id:
                    return result[1]
                else:
                    self.results_queue.put(result)
            else:
                await asyncio.sleep(0)  # Yield to other tasks

    async def read(self, table, keys, values):
        """
        Read rows from the database.
        :param table: Table to read from
        :param keys: Keys to read
        :param values: Values to match
        :return: Rows matching the query
        """
        transaction_id = uuid.uuid4()
        self.read_queue.put((table, keys, values, transaction_id))
        while True:
            if not self.results_queue.empty():
                result = self.results_queue.get()
                if result[0] == transaction_id:
                    return result[1]
                else:
                    self.results_queue.put(result)
            else:
                await asyncio.sleep(0)