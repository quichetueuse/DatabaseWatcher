import time

from DatabaseWatcher import DatabaseWatcher
import json

from DumpManager import DumpManager

database_watcher = DatabaseWatcher()

start_time = time.time()
database_dump = database_watcher.createDictionary()
# print(database_dump)

encrypted_dump = database_watcher.dump_manager.toJson(database_dump, True)

db_dump_json = json.dumps(database_dump, indent=4, ensure_ascii=False)
with (open('data.json', 'w', encoding='utf-8') as json_file):
    # json.dump(database_dump, json_file, indent=4, ensure_ascii=False) #, ensure_ascii=False
    json_file.write(encrypted_dump)
# print(db_dump_json)
print("--- %s seconds ---" % round((time.time() - start_time), 3))
