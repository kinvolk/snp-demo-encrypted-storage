import polars as pl
import polars.selectors as cs

import sys
from os import environ

import crypto


n = len(sys.argv)
if n < 3:
    print("Usage:\n\t", sys.argv[0], "CSV_FILE QUERY")
    sys.exit(1)

key = environ["KEY"]

df = (
        pl.scan_csv(sys.argv[1])
        .filter(pl.col("description") == sys.argv[2])
)

df = df.select(
        pl.col("description"),
        pl.col("secret").apply(lambda v: crypto.decrypt_val(key, v), pl.Utf8))

print(df.collect(streaming=True))
