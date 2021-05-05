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
    
    def __init__(self, connection, target=None):
        """[summary]
            The almighty Database class constructor. 
        Args:
            connection (Connection): Database connection object
            target (Type): The relational database management system to be used, defaults to None.
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
    
    def __init__(self, connection, target=None):
        """[summary]
        The almighty SQL class constructor. 
        Args:
            connection (Connection): Database connection object (e.g.  conn = sqlite3.connect('cookbook.db')).
            target (Type, optional): The relational database management system to be used, defaults to None.
        """
        super().__init__(connection,target)

    def get_last_id(self, table, id_column):
        """ Gets the last id (primary key value) of a table. This id is usually sequencial.
        Args:
            table (string): Name of the table you wish to get the last entry id (primary key value).
            id_column (string): Name of the primary key column.
        Returns:
            An integer that represents the unique value that identifies a row of a table.  
        """
        try:
            row = (self.__select("SELECT MAX(" + id_column + ") as id FROM "+ table))
            return(int(row["id"])) # Return the last id created on [table]
        except Exception as e:
            raise BadRequest(path=request.path,message=str(e), error="Database error", operation="Get last id", api="database", status=500)

    def execute(self, statement, args=None):
        """ Execute an SQL Statement
        Args:
            statement (string): The SQL statement to be executed against the database.
        Raises:
            BadRequest: Raises an exception if a database related error is catched.
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
        """ Table Structures - Table Structures related queries
        Args:
            statement (string): The SQL statement to be executed against the database.
        Raises:
            BadRequest: Raises an exception if a database related error is catched.
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(statement)
            self.connection.commit()
            cursor.close()
        except Exception as e:
            raise BadRequest(path=request.path,message=str(e), error="Database error", operation="SELECT", api="database")

    def __select(self, statement, args=None):
        """ Data Manipulation - SELECT
        Args:
            statement (string): The SELECT statement to be executed against the database.
            args (tuple): SQL statement arguments, defaults to None. 
        Returns:
            For n results, a list of dictionaries containing the results of the provided SQL statement.
            For 1 result, a dictionary containing the result of the provided SQL statement.
        Raises:
            BadRequest: Raises an exception if a database related error is catched.
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
        """ Data Manipulation - INSERT
        Args:
            statement (string): The INSERT statement to be executed against the database.
            args (tuple): SQL statement arguments.
        Returns:
            Returns the primary key value of the new entry.
        Raises:
            BadRequest: Raises an exception if a database related error is catched.
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
        """ Data Manipulation - UPDATE
        Args:
            statement (string): The UPDATE statement to be executed against the database.
            args (tuple): SQL statement arguments.
        Raises:
            BadRequest: Raises an exception if a database related error is catched.
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
        """ Data Manipulation - DELETE
        Args:
            statement (string): The DELETE statement to be executed against the database.
            args (tuple): SQL statement arguments.
        Raises:
            BadRequest: Raises an exception if a database related error is catched.
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
