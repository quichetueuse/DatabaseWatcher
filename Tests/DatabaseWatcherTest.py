from unittest import TestCase
from DatabaseWatcher import DatabaseWatcher


class DatabaseWatcherTest(TestCase):
    # TestCase that test every method in DatabaseWatcher class

    def test_getTableNames(self):
        db_watcher = DatabaseWatcher()
        tables = db_watcher._getAllTablesName()
        self.assertListEqual(tables, ['dumb_sentence', 'utilisateurs'])

    def test_getFieldsDictionary(self):
        db_watcher = DatabaseWatcher()
        fields_dictionary = db_watcher._generateFieldPatterns('dumb_sentence')
        self.assertListEqual(fields_dictionary, [{'field': 'id', 'type': 'int', 'null': 'NO', 'key': 'PRI', 'default': None, 'extra': 'auto_increment'}, {'field': 'sentence', 'type': 'varchar(256)', 'null': 'NO', 'key': '', 'default': None, 'extra': ''}, {'field': 'rating', 'type': 'varchar(8)', 'null': 'NO', 'key': '', 'default': None, 'extra': ''}, {'field': 'is_good', 'type': 'tinyint(1)', 'null': 'NO', 'key': '', 'default': '0', 'extra': ''}])
        
    def test_getRecordsDictionary(self):
        db_watcher = DatabaseWatcher()
        records_dictionary = db_watcher._generateRecordPatterns('dumb_sentence')
        self.assertListEqual(records_dictionary, [['1', "tu n'es pas le couteau le plus aiguisé du tirroir! ", '10/10', '1'], ['2', "tu n'es pas le pingouin qui glisse le mieux sur la banquise!", '8.5/10', '0'], ['3', "Tu es le genre de gars à prendre une bouteille vide au cas où tu n'as pas soif!", '6/10', '1'], ['4', "Tu respires l'intelligence mais tu as le nez bouché! ", '9.5/10', '1']])
        
    def test_getFullDictionary(self):
        db_watcher = DatabaseWatcher()
        full_dictionary = db_watcher.createDictionary()
        self.assertDictEqual(full_dictionary, {'tables': [{'name': 'dumb_sentence', 'fields': [{'field': 'id', 'type': 'int', 'null': 'NO', 'key': 'PRI', 'default': None, 'extra': 'auto_increment'}, {'field': 'sentence', 'type': 'varchar(256)', 'null': 'NO', 'key': '', 'default': None, 'extra': ''}, {'field': 'rating', 'type': 'varchar(8)', 'null': 'NO', 'key': '', 'default': None, 'extra': ''}, {'field': 'is_good', 'type': 'tinyint(1)', 'null': 'NO', 'key': '', 'default': '0', 'extra': ''}], 'records': [['1', "tu n'es pas le couteau le plus aiguisé du tirroir! ", '10/10', '1'], ['2', "tu n'es pas le pingouin qui glisse le mieux sur la banquise!", '8.5/10', '0'], ['3', "Tu es le genre de gars à prendre une bouteille vide au cas où tu n'as pas soif!", '6/10', '1'], ['4', "Tu respires l'intelligence mais tu as le nez bouché! ", '9.5/10', '1']]}, {'name': 'utilisateurs', 'fields': [{'field': 'id', 'type': 'int', 'null': 'NO', 'key': 'PRI', 'default': None, 'extra': 'auto_increment'}, {'field': 'last_name', 'type': 'varchar(32)', 'null': 'NO', 'key': '', 'default': None, 'extra': ''}, {'field': 'firs_name', 'type': 'varchar(32)', 'null': 'NO', 'key': '', 'default': None, 'extra': ''}, {'field': 'birth_date', 'type': 'date', 'null': 'NO', 'key': '', 'default': None, 'extra': ''}, {'field': 'gender', 'type': "enum('Homme','Femme')", 'null': 'YES', 'key': '', 'default': None, 'extra': ''}, {'field': 'comment', 'type': 'varchar(128)', 'null': 'NO', 'key': '', 'default': None, 'extra': ''}, {'field': 'admin', 'type': 'tinyint', 'null': 'NO', 'key': '', 'default': '0', 'extra': ''}], 'records': [['1', 'Doyle', 'Finley', '1994-05-04', 'Femme', '', '1'], ['2', 'O’Neal', 'Iris', '1975-01-17', 'Homme', 'not very dumb', '0'], ['3', 'Whitaker', 'Jerry', '2005-10-27', 'Homme', '', '0']]}]})
