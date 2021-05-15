""""""
"""     _e-e_
      _(-._.-)_
   .-(  `---'  )-. 
  __\ \\\___/// /__
 '-._.'/M\ /M\`._,-
 Froggy's database API
"""
from flask import request, jsonify
import froggy, sqlite3, json
from froggy.exceptions import BadRequest
from dataclasses import dataclass
from collections import namedtuple 
from typing import Any

@dataclass
class Type:
    """Database 'flavors'.
    """
    @dataclass 
    class Mysql: pass
    @dataclass
    class Sqlite3: pass

class Database():
    """The Database class represents a database of type :class:`froggy.database.Type`.
    """    
    def __init__(self, connection, target=None):
        """The Database class constructor.

        :param connection: Database connection object
        :type connection: Connection
        :param target: The relational database management system to be used, defaults to None
        :type target: Type
        """
        # Set the database type
        self.connection = connection
        if target == Type.Sqlite3:
            #self.connection.row_factory = sqlite3.Row # for row['id'] result access.
            self.connection.row_factory = self.dict_factory
        self.type = target

    def dict_factory(self, cursor, row):
        """Convert database results to a list of dictionaries. 
        """
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

class Query(Database):
    """The Query class represents a query object to be executed on a :class:`froggy.database.Database` object.
    """
    def __init__(self, connection, target=None):
        """The Query class constructor.

        :param connection: Database connection object (e.g.  conn = sqlite3.connect('cookbook.db')).
        :type connection: Connection
        :param target: The relational database management system to be used, defaults to None
        :type target: Type
        """
        super().__init__(connection,target)

    def get_last_id(self, table, id_column):
        """Gets the last id (primary key value) of a table. This id is usually sequencial.

        :param table: Name of the table you wish to get the last entry id (primary key value).
        :type table: str
        :param id_column:  Name of the primary key column.
        :type id_column: str
        :raises BadRequest: Raises a database error if something goes wrong.
        :return: An integer that represents the unique value that identifies a row of a table.
        :rtype: int
        """
        try:
            row = (self.__select("SELECT MAX(" + id_column + ") as id FROM "+ table))
            return(int(row["id"])) # Return the last id created on [table]
        except Exception as e:
            raise BadRequest(path=request.path,message=str(e), error="Database error", operation="Get last id", api="database", status=500)

    def execute(self, statement, args=None):
        """Execute an SQL Statement

        :param statement: The SQL statement to be executed against the database.
        :type statement: str
        :param args: The list of arguments for the SQL statement.
        :type args: list
        :raises BadRequest: Raises a database error if something goes wrong.
        :return: If the SQL statement is a SELECT then it returns a list of results; If the SQL statement is an INSERT then the id of the new entry is returned.
        :rtype: list or int
        """
        try:
            name = (statement[0:statement.index(" ")]).lower()
        except Exception as e:
            raise BadRequest(path=request.path,message=str(e), error="Please revise the SQL Query", operation="Query Processing", api="database")
        try:
            if ("select" in name):
                return self.__select(statement, args)
            if ("insert" in name):
                return self.__insert(statement, args)
            if ("update" in name):
                return self.__update(statement, args)
            if ("delete" in name):
                return self.__delete(statement, args)
            if ("create" in name or "alter" in name or 
                "drop" in name or "truncate" in name):
                return self.__table_structure(statement)
        except Exception as e:
            raise BadRequest(path=request.path,message=str(e), operation="Query Processing", api="database")
      
    def __table_structure(self, statement):
        """Table Structures - Table Structures related queries

        :param statement: The SQL statement to be executed against the database.
        :type statement: str
        :raises BadRequest: Raises an exception if a database related error is catched.
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(statement)
            self.connection.commit()
            cursor.close()
        except Exception as e:
            raise BadRequest(path=request.path,message=str(e), error="Database error", operation="SELECT", api="database")

    def __select(self, statement, args=None):
        """Data Manipulation - SELECT

        :param statement: The SELECT statement to be executed against the database.
        :type statement: str
        :param args: SQL statement arguments, defaults to None.
        :type args: list, optional
        :raises BadRequest: Raises an exception if a database related error is catched.
        :return: For n>1 results, returns a list of dics containing the results of the provided SQL statement. Otherwise, returns a dic containing the result of the provided SQL statement.
        :rtype: list of dics or dic
        """
        try:
            # Returns a list of dics as the result of a sql statement
            cursor = self.connection.cursor()
            # Execute the SQL Select Statement.
            if (args is not None):
                cursor.execute(statement, args)
            else:
                cursor.execute(statement)

            res = cursor.fetchall()
            cursor.close()
            
            froggy.gadgets.fprint("SQL statement executed  :" + str(statement))
            froggy.gadgets.fprint("SQL statement arguments :" + str(args))
            # If there is only one result, lets just return an dic instead of a list of dics
            if (len(res) == 1): res = res[0]
            # 'You complete me.'
            return(res)
        except Exception as e:
            raise BadRequest(path=request.path,message=str(e), error="Database error", operation="SELECT", api="database")

    def __insert(self, statement, args):
        """Data Manipulation - INSERT

        :param statement: The INSERT statement to be executed against the database.
        :type statement: str
        :param args: SQL statement arguments.
        :type args: list
        :raises BadRequest: Raises an exception if a database related error is catched.
        :return: Returns the id of the new entry.
        """
        try:

            cursor = self.connection.cursor()
            # Execute the SQL statement with 'args'
            cursor.execute(statement, args)
            # Get the last created id after executing the SQL statement.
            # This is useful to get primary key values that were set as auto-increment.
            created_id = -1
            
            if (self.type == Type.Mysql): created_id = self.connection.insert_id()
            if (self.type == Type.Sqlite3): created_id = cursor.lastrowid
                        
            # Save (commit) the changes and close the cursor
            self.connection.commit()
            cursor.close()

            froggy.gadgets.fprint("SQL statement executed  :" + statement)
            froggy.gadgets.fprint("SQL statement arguments :" + str(args))
            froggy.gadgets.fprint("Last inserted ID        :" + str(created_id))
            # 'You make me want to be a better man.'
            return({"id:": created_id})
        except Exception as e:
            raise BadRequest(path=request.path,message=str(e), error="Database error", operation="INSERT", api="database")

    def __update(self, statement, args):
        """Data Manipulation - UPDATE.

        :param statement: The UPDATE statement to be executed against the database.
        :type statement: str
        :param args: SQL statement arguments.
        :type args: list
        :raises BadRequest: Raises an exception if a database related error is catched.
        """
        try:
            cursor = self.connection.cursor() 
            froggy.gadgets.fprint("SQL statement executed :" + statement)
            froggy.gadgets.fprint("SQL values parsed      :" + str(args))
            # Execute the SQL statement with 'values'
            cursor.execute(statement, args)
            # Save (commit) the changes and close the cursor
            self.connection.commit()
            cursor.close()
        except Exception as e:
            raise BadRequest(path=request.path,message=str(e), error="Database error", operation="UPDATE", api="database")

    def __delete(self, statement, args):
        """Data Manipulation - DELETE.

        :param statement: The DELETE statement to be executed against the database.
        :type statement: str
        :param args: SQL statement arguments.
        :type args: list
        :raises BadRequest: Raises an exception if a database related error is catched.
        """
        try:
            cursor = self.connection.cursor() 
            froggy.gadgets.fprint("SQL statement executed :" + statement)
            froggy.gadgets.fprint("SQL values parsed      :" + str(args))
            # Execute the SQL statement with 'args'
            cursor.execute(statement, args)
            # Save (commit) the changes and close the cursor
            self.connection.commit()
            cursor.close()
        except Exception as e:
            raise BadRequest(path=request.path,message=str(e), error="Database error", operation="DELETE", api="database")
