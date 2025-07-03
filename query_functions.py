from utils import PriceHolder


def query_total(con, file, where_clause, params):
    return con.execute(
        f"SELECT COUNT(*) FROM '{file}' {where_clause}", params
    ).fetchone()[0]


def query_column_uniques(con, file, column, where_clause, params):
    query = f"""
        SELECT DISTINCT "{column}"
        FROM '{file}'
        {where_clause}
        ORDER BY "{column}"
    """
    return [row[0] for row in con.execute(query, params).fetchall()]


def query_filtered_data(
    con, file, where=[], sorting=None, price_qty=100, limit=25, page=1
):
    where_clause = ""
    idx = 0
    params = []
    for w in where.keys():
        val = where[w]

        if val is None:
            continue

        if w in ["Description", "MFR.Part", "LCSC Part"]:
            comb = " OR " if w in ["MFR.Part", "LCSC Part"] else " AND "
            tmp = f'"{w}" LIKE ?'
            if isinstance(val, list) or isinstance(val, tuple):
                placeholder = f"({comb.join([tmp]*len(val))})"
                params.extend([f"{v}" for v in val])
            else:
                placeholder = tmp
                params.append(f"{val}")

            if idx == 0:
                where_clause += f" WHERE {placeholder}"
            else:
                where_clause += f" AND {placeholder}"

            # print(where_clause)
            # print(params)

        else:
            if w == "Stock":
                placeholder = ">= ?"
                params.append(val)
            else:
                if w == "Library Type" and (
                    val == ["Basic", "Extended"] or val == ["Extended", "Basic"]
                ):
                    # Nothing to do
                    continue

                if isinstance(val, list) or isinstance(val, tuple):
                    placeholder = "IN (" + ",".join(["?"] * len(val)) + ")"
                    params.extend(val)
                else:
                    placeholder = "= ?"
                    params.append(val)

            if idx == 0:
                where_clause += f' WHERE "{w}" {placeholder}'
            else:
                where_clause += f' AND "{w}" {placeholder}'

        idx += 1

    if sorting:
        order_clause = (
            f'ORDER BY "{sorting[0]}" {"ASC" if sorting[1] == 'asc' else "DESC"}'
        )
    else:
        order_clause = ""

    total = query_total(con, file, where_clause, params)
    first = query_column_uniques(con, file, "First Category", where_clause, params)
    second = query_column_uniques(con, file, "Second Category", where_clause, params)
    pkg = query_column_uniques(con, file, "Package", where_clause, params)
    mfg = query_column_uniques(con, file, "Manufacturer", where_clause, params)

    if limit:
        limit_clause = f"LIMIT {limit} OFFSET {(page-1)*limit}"
    else:
        limit_clause = ""

    data = con.execute(
        f"SELECT * FROM '{file}' {where_clause} {order_clause} {limit_clause}",
        params,
    ).fetchdf()

    data["PriceMap"] = [PriceHolder(p) for p in data["Price"].values]
    data.loc[:, "Price"] = data.loc[:, "PriceMap"].apply(lambda fn: fn(price_qty))
    if sorting and sorting[0] == "Price":
        data.sort_values("Price", ascending=sorting[1] == "asc", inplace=True)
        data.reset_index(drop=True, inplace=True)
    data["Price"] = data["Price"].apply(lambda x: f"{x:.2f}")
    price_tooltips = data["PriceMap"].astype(str).tolist()

    return (
        total,
        first,
        second,
        pkg,
        mfg,
        price_tooltips,
        data.drop(columns=["PriceMap"]),
    )
