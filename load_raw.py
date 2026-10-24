import sys
from pathlib import Path

import duckdb


DB_PATH = "warehouse.duckdb"


def main():
    if len(sys.argv) != 2:
        print("Usage: python load_raw.py <csv_file>")
        sys.exit(1)

    csv_path = Path(sys.argv[1])

    if not csv_path.exists():
        print(f"Erreur : fichier introuvable : {csv_path}")
        sys.exit(1)

    con = duckdb.connect(DB_PATH)

    try:
        con.execute("CREATE SCHEMA IF NOT EXISTS raw")

        con.execute("DROP TABLE IF EXISTS raw.orders")

        con.execute("""
            CREATE TABLE raw.orders (
                order_id VARCHAR,
                order_date VARCHAR,
                customer_id VARCHAR,
                country VARCHAR,
                product VARCHAR,
                quantity VARCHAR,
                unit_price VARCHAR,
                _row_number BIGINT,
                _source_file VARCHAR,
                _loaded_at TIMESTAMP
            )
        """)

        con.execute("""
            INSERT INTO raw.orders (
                order_id,
                order_date,
                customer_id,
                country,
                product,
                quantity,
                unit_price,
                _row_number,
                _source_file,
                _loaded_at
            )
            SELECT
                order_id,
                order_date,
                customer_id,
                country,
                product,
                quantity,
                unit_price,
                row_number() OVER () AS _row_number,
                ? AS _source_file,
                current_timestamp AS _loaded_at
            FROM read_csv(
                ?,
                header = true,
                all_varchar = true,
                nullstr = ''
            )
        """, [str(csv_path), str(csv_path)])

        count = con.execute(
            "SELECT COUNT(*) FROM raw.orders"
        ).fetchone()[0]

        print(f"Fichier chargé : {csv_path}")
        print(f"Nombre de lignes chargées : {count}")
        print(f"Base DuckDB : {DB_PATH}")
        print("Table créée : raw.orders")

    finally:
        con.close()


if __name__ == "__main__":
    main()