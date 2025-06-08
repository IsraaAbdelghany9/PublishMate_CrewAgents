# sitecustomize.py
import sys
import pysqlite3

sys.modules["sqlite3"] = pysqlite3
sys.modules["pysqlite3"] = pysqlite3
