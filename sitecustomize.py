# sitecustomize.py

import sys
import importlib

# Force use of pysqlite3 as sqlite3
import pysqlite3
sys.modules["sqlite3"] = pysqlite3
sys.modules["pysqlite3"] = pysqlite3

# Optional: confirm override (remove this in production)
# print("✅ Patched sqlite3 with pysqlite3")
