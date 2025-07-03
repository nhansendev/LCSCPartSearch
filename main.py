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

import io
import os
import duckdb
import zipfile
import pandas as pd
import streamlit as st
from streamlit_components import (
    generic_select_table,
    generic_search_bar,
    libr_selector,
    main_table,
)
from query_functions import query_filtered_data
from streamlit_functions import session_init, reset_all
from utils import sql_to_saved_df

con = duckdb.connect(database=":memory:")

st.markdown(
    """
    <style>
        .block-container {
            padding-top: 1rem !important;
        }
        
        .center-button-container {
            display: flex;
            flex-direction: column;
            justify-content: center;
            height: 15px; /* Adjust height to control vertical space */
        }
    </style>
""",
    unsafe_allow_html=True,
)


def prepare_download():
    # Provide a download of the current filtered/sorted data as an Excel xlsx file
    total, first, second, pkg, mfg, price_tooltips, df = query_filtered_data(
        con,
        FILE,
        st.session_state.where,
        st.session_state.sort_params,
        st.session_state.price_qty,
        limit=None,
    )

    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False)
    buffer.seek(0)
    return buffer.getvalue()
    # return df.to_csv().encode("utf-8")


# Build Layout
st.set_page_config("LCSC Parts Database", layout="wide")

FILE = "stock.parquet"
if FILE and FILE.endswith("zip"):
    ex_file = FILE.replace("zip", "parquet")
    if not os.path.exists(ex_file):
        # Extract
        try:
            with zipfile.ZipFile(FILE, "r") as zip_ref:
                zip_ref.extractall(".")
        except zipfile.BadZipFile:
            print(f"Error: '{FILE}' is not a valid ZIP file.")
        except FileNotFoundError:
            print(f"Error: The file '{FILE}' was not found.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    FILE = ex_file

if not FILE:
    with st.spinner("Preparing Database...", show_time=True):
        FILE = r"C:\Users\nate\Documents\KiCad\9.0\3rdparty\plugins\com_github_bouni_kicad-jlcpcb-tools\jlcpcb\parts-fts5.db"
        # If prepared database file doesn't exist, then make it
        FILE = sql_to_saved_df(FILE)
PAGE_SIZE = 25

# Setup session_state
session_init()

# Main function for querying the database
total, first, second, pkg, mfg, price_tooltips, df = query_filtered_data(
    con,
    FILE,
    st.session_state.where,
    st.session_state.sort_params,
    st.session_state.price_qty,
    page=st.session_state.page + 1,
    limit=PAGE_SIZE,
)

# TODO: refine approach
# Conditional updating of the displayed filter options
if st.session_state.where.get("First Category") is None:
    st.session_state.filter_data["First Category"] = first

if st.session_state.where.get("Second Category") is None:
    st.session_state.filter_data["Second Category"] = second

if st.session_state.where.get("Package") is None:
    st.session_state.filter_data["Package"] = pkg

if st.session_state.where.get("Manufacturer") is None:
    st.session_state.filter_data["Manufacturer"] = mfg

# print(st.session_state.where)
# print([f"{k}:{len(v)}" for k, v in st.session_state.filter_data.items()])

st.header("LCSC Parts Database")

colwidths = [0.2, 0.3, 0.3, 0.2]

# Row 1
cols = st.columns(colwidths)

generic_select_table(cols[0], "Manufacturer", width=400)
generic_select_table(cols[1], "First Category", single=False)
generic_select_table(cols[2], "Second Category")
generic_select_table(cols[3], "Package", "Packages", width=400)

# Add a small spacer row
st.text("")

# Row 2
cols = st.columns(colwidths)

generic_search_bar(
    cols[0],
    "MFR.Part",
    label="MFG PN Search:",
    single=False,
    width=400,
)

generic_search_bar(
    cols[1],
    "Description",
    label="Search Description:",
    single=False,
    width=600,
)

subcol = cols[2].columns(3)
qty = subcol[0].number_input(
    "Price Quantity:",
    1,
    value=100,
    width=175,
    key="qty_input" + str(st.session_state.reset_flag),
)
if st.session_state.price_qty != qty:
    st.session_state.price_qty = qty
    st.session_state.rerun_flag = True

stock = subcol[1].number_input(
    "Stock Quantity (min):",
    0,
    value=1,
    width=175,
    key="stock_input" + str(st.session_state.reset_flag),
)
if st.session_state.where["Stock"] != stock:
    st.session_state.where["Stock"] = stock
    st.session_state.rerun_flag = True

libr_selector(subcol[2])

subcol = cols[3].columns([0.2, 0.4, 0.4])

subcol[0].markdown('<div class="center-button-container">', unsafe_allow_html=True)
reset_btn = subcol[0].button("Reset", type="primary", on_click=reset_all)
subcol[0].markdown("</div>", unsafe_allow_html=True)

subcol[1].markdown('<div class="center-button-container">', unsafe_allow_html=True)
if subcol[1].button("Prepare Download"):
    with subcol[2], st.spinner("Preparing Download...", show_time=True):
        dld_data = prepare_download()
    subcol[2].markdown('<div class="center-button-container">', unsafe_allow_html=True)
    download_btn = subcol[2].download_button(
        "Download Table",
        data=dld_data,
        file_name="parts_table.xlsx",
        on_click="ignore",
        type="primary",
        icon=":material/download:",
    )
    subcol[2].markdown("</div>", unsafe_allow_html=True)
subcol[1].markdown("</div>", unsafe_allow_html=True)

st.text("")

cols = st.columns(colwidths)

generic_search_bar(
    cols[0],
    "LCSC Part",
    label="LCSC PN Search:",
    single=False,
    width=400,
)

cols[1].text(
    'Part number and description searches use ";" delimiters and "%" as wildcard.\nPart number search: match ANY terms\nDescription search: match ALL terms'
)

cols[3].text("Hover over prices for price levels, if available.")

part_label = st.write(f"Found: {total} part(s)")

main_table(df, int(total / PAGE_SIZE) + 1, tooltips={"Price": price_tooltips})

if st.session_state.rerun_flag:
    st.session_state.rerun_flag = False
    st.rerun()
