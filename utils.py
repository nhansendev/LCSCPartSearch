"""
MIT License

Copyright (c) 2025 Nathan Hansen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import sqlite3
import numpy as np
import pandas as pd


def sql_to_saved_df(db_path, replace=False):
    outpath = os.path.join(os.getcwd(), "full_db.parquet")
    if not replace and os.path.exists(outpath):
        return outpath

    conn = sqlite3.connect(db_path)
    query = "SELECT * FROM parts;"
    raw_df = pd.read_sql_query(query, conn)
    raw_df.drop(columns=["Datasheet"], inplace=True)
    raw_df["Stock"] = raw_df["Stock"].astype(int)
    conn.close()
    print("Saved to:", outpath)
    raw_df.to_parquet(outpath)
    return outpath


def _value_to_str(value, unit=""):
    # Round to the nearest third order of magnitude (1, 3, 6, ...)
    mag = np.floor(np.log10(abs(value)) / 3)
    suf = "pnum kMG"[int(mag + 4)]
    vstr = f"{value*10**(-mag*3):.2f}".rstrip("0").rstrip(".")
    return f'{vstr}{suf if suf != " " else ""}{unit}'


class PriceHolder:
    def __init__(self, pricemap):
        if isinstance(pricemap, str):
            if len(pricemap) > 0:
                self.pricemap = _price_str_to_list(pricemap)
            else:
                self.pricemap = None
        else:
            self.pricemap = pricemap

    def get_price(self, qty):
        if self.pricemap is None:
            return -1

        for r, v in self.pricemap:
            if qty >= r[0] and (r[1] is None or qty <= r[1]):
                return qty * v

        # Out of range
        return -1

    def __call__(self, qty):
        return self.get_price(qty)

    def __repr__(self):
        if self.pricemap is None:
            return "No Data"
        out = []
        for (st, en), val in self.pricemap:
            v2 = "+" if en is None else f" - {en}"
            valstr = f"{val:.3f}".rjust(3)
            out.append(f"{valstr}  |  {st}{v2}")
        return "- " + "\n- ".join(out)


def _price_str_to_list(pstr):
    levels = []
    for a in pstr.split(","):
        rng, cost = a.split(":")
        st, en = rng.split("-")
        rng = [int(st), int(en) if len(en) > 0 else None]
        levels.append([rng, float(cost)])
    return levels


def _find(segments, indicator):
    for seg in segments:
        if indicator in seg:
            return seg
    return ""


def _rval_to_float(val):
    prefix_map = {"p": -12, "n": -9, "u": -6, "m": -3, "k": 3, "M": 6}
    tmp = val.replace("Ω", "")
    for i in range(1, len(tmp) + 1):
        try:
            float(tmp[: i + 1])
        except ValueError:
            break

    fval = float(tmp[:i])
    if i < len(tmp):
        mval = prefix_map.get(tmp[i], 0)
        return fval * 10**mval
    else:
        return fval


class OrderedSet:
    def __init__(self, values=None):
        self.data = []
        if values is not None:
            for v in values:
                self.add(v)

    def __len__(self):
        return len(self.data)

    def __contains__(self, value):
        return value in self.data

    def __iter__(self):
        for v in self.data:
            yield v

    def add(self, value):
        if value not in self.data:
            self.data.append(value)

    def remove(self, value):
        if value in self.data:
            self.data.remove(value)

    def replace(self, old_value, new_value):
        if old_value in self.data and new_value not in self.data:
            self.data[self.data.index(old_value)] = new_value

    def __repr__(self):
        return str(self.data)
