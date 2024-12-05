

class DatabaseWatcher:

    def didDatabaseChanged(self):
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