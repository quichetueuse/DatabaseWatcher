import colorama

from DatabaseWatcher import DatabaseWatcher
import time


def backupDatabase():
    database_watcher = DatabaseWatcher("Tests/config_tests.ini")
    database_watcher.dumpDatabase()


def readFromBackup():
    database_watcher = DatabaseWatcher("Tests/config_tests.ini")
    database_watcher.compareTables()


if __name__ == "__main__":
    print(colorama.Fore.RED + "Message in this color give information about an error" + colorama.Fore.RESET)
    print(colorama.Fore.BLUE + "Message in this color give useful informations" + colorama.Fore.RESET)
    print("\n")
    start_time = time.time()
    # Backup database
    # backupDatabase()
    # Create database from backuo
    readFromBackup()
    print("--- The program ran in %s seconds ---" % round((time.time() - start_time), 3))
