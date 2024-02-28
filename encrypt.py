import polars as pl
import crypto

df = pl.scan_csv("df.csv")

key = crypto.new_key()

df_enc = (df.select([
    pl.exclude('secret'),
    pl.col('secret').apply(lambda v: crypto.encrypt_val(key, v)),
])).collect(streaming=True)

with open("df_enc.key", "wb") as f: f.write(key)
with open("df_enc.csv", "w") as f: df_enc.sink_csv(f)
