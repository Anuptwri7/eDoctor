import sqlite3
import sys
import django

print("Python version:", sys.version)
print("Django version:", django.get_version())
print("SQLite3 version:", sqlite3.sqlite_version)
