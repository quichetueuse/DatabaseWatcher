from datetime import datetime, date, time
from decimal import Decimal
from typing import List

from ConfigManager import ConfigManager
from DatabaseManager import DatabaseManager
from DumpManager import DumpManager


class DatabaseWatcher:

    def __init__(self):
        # Loading configuration manager class
        self.config_manager = ConfigManager()

        # instancing other app components
        self.database_manager = DatabaseManager(config_manager=self.config_manager)
        self.dump_manager = DumpManager(config_manager=self.config_manager)

        # Defining pattern for data
        # self.table_pattern: dict = {"name": None, "fields": [], "records": []}
        # self.field_pattern: dict = {"field": None, "type": None, "null": True, "key": None, "default": None, "extra": None}
        # self.record_pattern: dict = {"field": None, "value": None}

    def createDictionary(self) -> dict:
        database_dump: dict = {'tables': []}

        # Getting all the tables name in selected database
        tables_name = self._getAllTablesName()

        # Looping through each table
        for table in tables_name:
            # Getting a copy of table pattern
            table_pattern = {"name": None, "fields": [], "records": []}

            # Filling blank pattern
            table_pattern["name"] = table

            # Getting every field from current table
            fields = self.database_manager._getFieldsFromTable(table=table)

            field_patterns: list[dict] = []

            fields_name: List[str] = []
            # Looping through fields list from current table
            for field in fields:
                # Getting a copy of field pattern
                field_pattern = {"field": None, "type": None, "null": True, "key": None, "default": None, "extra": None}

                fields_name.append(field[0])

                # Filling blank pattern
                field_pattern['field'] = field[0] # todo optimiser ca avec un for
                field_pattern['type'] = field[1]
                field_pattern['null'] = field[2]
                field_pattern['key'] = field[3]
                field_pattern['default'] = field[4]
                field_pattern['extra'] = field[5]

                # Appending pattern to pattern list
                field_patterns.append(field_pattern)
                field_pattern = None

            table_pattern['fields'] = field_patterns

            records = self.database_manager._getRecordsFromTable(table=table)

            record_values: List[List[dict]] = []

            # Looping through each record from current table
            for record in records:
                record_fields: List[dict] = []
                # Looping from each field name in table
                for i, field in enumerate(fields_name):
                    # Getting a copy of record pattern
                    record_pattern = {"field": None, "value": None}

                    record_pattern['field'] = field
                    # if isinstance(record[i], (datetime, date, time, Decimal)):
                    #     value = str(record[i])
                    # else:
                    #     value = record[i]
                    # record_pattern['value'] = value
                    record_pattern['value'] = str(record[i])

                    record_fields.append(record_pattern)

                record_values.append(record_fields)
            table_pattern['records'] = record_values

            database_dump['tables'].append(table_pattern)

        return database_dump


    def _generateFieldPatterns(self, table: str) -> List[dict]:
        # Getting every field from current table
        fields = self.database_manager._getFieldsFromTable(table=table)

        # List that will store all the field patterns
        field_patterns: list[dict] = []

        for field in fields:
            # Getting a copy of field pattern
            field_pattern = {"field": None, "type": None, "null": True, "key": None, "default": None, "extra": None}

            # fields_name.append(field[0])

            # Filling blank pattern
            field_pattern['field'] = field[0]  # todo optimiser ca avec un for
            field_pattern['type'] = field[1]
            field_pattern['null'] = field[2]
            field_pattern['key'] = field[3]
            field_pattern['default'] = field[4]
            field_pattern['extra'] = field[5]

            # Appending pattern to pattern list
            field_patterns.append(field_pattern)

        return field_patterns


    def _getAllTablesName(self):

        raw_tables: List[tuple] = self.database_manager._getAllTables()

        # Getting only tables name
        tables_name: List[str] = [raw_table[0] for raw_table in raw_tables]
        return tables_name

    # def _getAllFieldsFromTable(self, table) -> List[tuple]:
    #     return self.database_manager._getFieldsFromTable(table=table)

    def didDatabaseChanged(self):
        pass

    def dumpDatabase(self):
        pass


    def restoreDatabase(self):
        pass


#SELECT User FROM mysql.user;
#SHOW FIELDS FROM mysql.user;
#SHOW TABLES;

#https://stackoverflow.com/questions/201621/how-do-i-see-all-foreign-keys-to-a-table-or-column

"""
select concat(fks.constraint_schema, '.', fks.table_name) as foreign_table,
       '->' as rel,
       concat(fks.unique_constraint_schema, '.', fks.referenced_table_name)
              as primary_table,
       fks.constraint_name,
       group_concat(kcu.column_name
            order by position_in_unique_constraint separator ', ') 
             as fk_columns
from information_schema.referential_constraints fks
join information_schema.key_column_usage kcu
     on fks.constraint_schema = kcu.table_schema
     and fks.table_name = kcu.table_name
     and fks.constraint_name = kcu.constraint_name
-- where fks.constraint_schema = 'database name'
group by fks.constraint_schema,
         fks.table_name,
         fks.unique_constraint_schema,
         fks.referenced_table_name,
         fks.constraint_name
order by fks.constraint_schema,
         fks.table_name;


"""
# SHOW CREATE TABLE `<yourtable>`;

# SELECT * FROM information_schema.TABLE_CONSTRAINTS
# WHERE information_schema.TABLE_CONSTRAINTS.CONSTRAINT_TYPE = 'FOREIGN KEY'
# AND information_schema.TABLE_CONSTRAINTS.TABLE_NAME = 'clients';


# get all foreign keys : select * from INFORMATION_SCHEMA.TABLE_CONSTRAINTS where CONSTRAINT_TYPE = 'FOREIGN KEY';