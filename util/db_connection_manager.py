"""db_connection_manager.py

Contains a class that manages the connection to the database.
"""

import asyncpg

from util.printing import print_petrichor_msg

import os

from discord import Interaction
from asyncpg import Record
from asyncpg.pool import PoolAcquireContext



class DatabaseConnectionManager:
    """
    Class that contains logic for database connection and operations.

    This class should only be run in the `async with` statement, like so:
    ```
    async with DatabaseConnectionManager() as db:
        pass
    ```

    Attributes
    ----------
    PSQL_DATATYPE_MAP : dict[str, str]
        mapping of PostgreSQL data types to python primitive types
    """

    def __init__(self):
        self.PSQL_DATATYPE_MAP : dict[str, str] = {
            'bigint'        : 'int',
            'bigserial'     : 'int',
            'bit'           : 'int',
            'bit varying'   : 'int',
            'boolean'       : 'bool',
            'box'           : 'str',
            'bytea'         : 'bytearray',
            'character'     : 'str',
            'character varying' : 'str',
            'cidr'          : 'str',
            'circle'        : 'str',
            'date'          : 'str',
            'double precision'  : 'float',
            'inet'          : 'str',
            'integer'       : 'int',
            'interval'      : 'str',
            'json'          : 'str',
            'jsonb'         : 'bytes',
            'line'          : 'str',
            'lseg'          : 'str',
            'macaddr'       : 'str',
            'macaddr8'      : 'str',
            'money'         : 'float',
            'numeric'       : 'float',
            'path'          : 'str',
            'pg_lsn'        : 'int',
            'pg_snapshot'   : 'str',
            'point'         : 'str',
            'polygon'       : 'str',
            'real'          : 'float',
            'smallint'      : 'int',
            'smallserial'   : 'int',
            'serial'        : 'int',
            'text'          : 'str',
            'time'          : 'str',
            'time with time zone'       : 'str',
            'timestamp'     : 'str',
            'timestamp with time zone'  : 'str',
            'tsquery'       : 'str',
            'tsvector'      : 'str',
            'uuid'          : 'str',
            'xml'           : 'str'
        }


    async def __aenter__(self):
        # postgres://user:pass@host:port/database?option=value
        self._db_pool = await asyncpg.create_pool(
            dsn=(
                f'postgres://'
                f'{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASS')}'
                f'@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}'
                f'/{os.getenv('POSTGRES_DB')}'
            )
        )
        print_petrichor_msg('Connected to database!')
        return self


    async def __aexit__(self, *args, **kwargs):
        await self._db_pool.__aexit__(*args, **kwargs)



    async def ping_tables(self) -> None:
        """
        Displays the names of the tables in the petrichor database.
        Generally used to ensure that the database connection is 
        properly established.
        """
        tables = await self._fetch_query((
            'SELECT table_name '
            'FROM information_schema.tables '
            "WHERE table_schema = 'public' "
            f"AND table_type='BASE TABLE'"
        ))
        print_petrichor_msg(f"Tables: {[table['table_name'] for table in tables]}")
                

    # async def insert_row(
    #     self, 
    #     table_name : str, 
    #     interaction : Interaction
    # ) -> None:
    async def insert_row(
        self, 
        table_name : str, 
        record_info : list
    ) -> None:
        """
        Inserts a row into a given database. It is assumed that `record_info`
        contains properly formatted data—that is, each item in the list
        matches up with its corresponding column in the table `table_name`.
        
        Parameters
        ----------
        table_name : str
            the name of the table to run the INSERT query
        record_info : list
            the data to insert into the table
        """

        # get from interaction
        # record_info = [] 
        query = await self._generate_insert_query(table_name, record_info)
        await self._execute_query(query)

        print_petrichor_msg(f'Row inserted into {table_name}')


    async def _get_table_column_info(
        self, 
        table_name : str
    ) -> list[tuple[str, str]]:
        """
        Gets the name and datatype of every column in a given table.

        Parameters
        ----------
        table_name : str
            the name of the table to get the data of

        Returns
        -------
        list[tuple[str, str]]
            a list of (column_name, data_type) tuples
        """
        
        columns = await self._fetch_query((
            'SELECT column_name, data_type '
            'FROM information_schema.columns '
            f"WHERE table_name = '{table_name}' "
            'ORDER BY ordinal_position;'
        ))

        return [
            (column['column_name'], column['data_type']) 
            for column in columns
        ]


    async def _generate_insert_query(
        self, 
        table_name : str, 
        record_info : list
    ) -> str:
        """
        Generates an INSERT query given a table name and data to insert into
        a row.
        
        Parameters
        ----------
        table_name : str
            the name of the table to insert into
        record_info : list
            the information to add into the row
        
        Returns
        -------
        str
            the generated INSERT query
        """
        
        table_column_info = await self._get_table_column_info(table_name)

        columns = [
            str(column_info[0]) 
            for column_info 
            in table_column_info
            if column_info[1] != 'uuid'  # uuid column doesn't go in INSERT
        ]

        values = []
        index = 0
        for column_info in table_column_info:

            # skip uuid column, since this is automatically filled by PSQL
            if column_info[1] == 'uuid':
                continue
            
            values.append(
                self._wrap_data(
                    data_type=column_info[1], 
                    data=str(record_info[index])
                )
            )
            index += 1
            

        return (
            f'INSERT INTO {table_name} ({", ".join(columns)}) '
            f'VALUES ({", ".join(values)});'
        )
    

    def _wrap_data(self, data_type : str, data : str) -> str:
        """
        Wraps the given data in single quotes, if necessary.
        
        Parameters
        ----------
        data_type : str
            the PostgreSQL data type that the given data has
        data : str
            the given 
        
        Returns
        -------
        str
            the data wrapped in single quotes, if necessary

        Notes
        -----
        At the moment, all used data types can be properly type casted by
        PostgreSQL, even if just wrapped in single quotes. As such, this method
        simply returns all given data with a wrap in single quotes.
        """

        # match self.PSQL_DATATYPE_MAP[data_type]:
        #     case 'str': return f"'{data}'"
        #     case 'int' | 'float' | 'bool': return data
        #     case _: return 'NO DATA MAPPING'
        return f"'{data}'"


    async def _fetch_query(self, query : str) -> list[Record]:
        """
        Performs a query and returns its results.
        
        Parameters
        ----------
        query : str
            the PostgreSQL query to run
        
        Returns
        -------
        list[Record]
            the fetched rows
        """

        conn : PoolAcquireContext
        async with self._db_pool.acquire() as conn:
            async with conn.transaction():
                return await conn.fetch(query)


    async def _execute_query(self, query : str) -> None:
        """
        Performs a query.

        Parameters
        ----------
        query : str
            the PostgreSQL query to run
        """

        conn : PoolAcquireContext
        async with self._db_pool.acquire() as conn:
            async with conn.transaction():
                return await conn.execute(query)
