import sys
import duckdb

con = duckdb.connect("warehouse.duckdb", read_only=True)

try:
    con.sql(sys.argv[1]).show()
finally:
    con.close()