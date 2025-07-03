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

import numpy as np
import pandas as pd
import streamlit as st
from sortable_table import sortable_table

# from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode


def generic_select_table(
    container, name, label=None, single=False, width=600, height=250
):
    def _callback():
        # We want the dataframe to output selection info, but not call rerun,
        # So a placeholder callback is needed
        pass

    if label is None:
        label = name

    table = container.dataframe(
        pd.DataFrame({label: st.session_state.filter_data[name]}),
        width=width,
        height=height,
        use_container_width=False,
        hide_index=True,
        on_select=_callback,
        selection_mode="single-row" if single else "multi-row",
        key=name + str(st.session_state.reset_flag),
    )

    if table["selection"]["rows"]:
        tmp = st.session_state.filter_data[name]
        if single:
            new_where = tmp[table["selection"]["rows"][0]]
        else:
            new_where = [tmp[s] for s in table["selection"]["rows"]]
    else:
        new_where = None

    if new_where != st.session_state.where[name]:
        st.session_state.where[name] = new_where
        st.session_state.rerun_flag = True


def generic_search_bar(container, name, value="", label=None, single=True, width=600):
    if label is None:
        label = name

    sbar = container.text_input(
        label, value=value, width=width, key=name + str(st.session_state.reset_flag)
    )

    if len(sbar) > 0:
        if single:
            new_where = sbar
        else:
            new_where = [s.strip() for s in sbar.split(";")]
            new_where = [v for v in np.unique(new_where) if len(v) > 0]
            if len(new_where) < 1:
                # No valid strings
                new_where = None
    else:
        new_where = None

    if new_where != st.session_state.where[name]:
        st.session_state.where[name] = new_where
        st.session_state.rerun_flag = True


def main_table(df, max_page, tooltips=None):
    st.session_state.retrigger = not st.session_state.retrigger

    if not st.session_state.sort_params:
        sort_col = None
        sort_dir = "asc"
    else:
        sort_col, sort_dir = st.session_state.sort_params

    sort_event = sortable_table(
        data=df,
        sort_column=sort_col,
        sort_direction=sort_dir,
        max_page=max_page,
        column_widths=[
            "5%",
            "12%",
            "12%",
            "10%",
            "8%",
            "4%",
            "10%",
            "4%",
            "",
            "4%",
            "4%",
        ],
        key="custom_df",
        max_height="700px",
        retrigger=st.session_state.retrigger,
        style_overrides="--font-size: 14px;",
        cell_tooltips=tooltips,
    )

    if st.session_state.page != sort_event["page"]:
        st.session_state.page = sort_event["page"]
        st.session_state.rerun_flag = True

    sort_info = sort_event["sort"]
    if sort_info:
        info = [sort_info["column"], sort_info["direction"]]
        if info != st.session_state.sort_params:
            st.session_state.sort_params = info
            st.session_state.rerun_flag = True
    else:
        if st.session_state.sort_params:
            st.session_state.sort_params = None
            st.session_state.rerun_flag = True


def libr_selector(container):
    libr = container.segmented_control(
        "Library Type:",
        ["Basic", "Extended"],
        selection_mode="multi",
        default=st.session_state.where["Library Type"] or ["Basic", "Extended"],
        key="libr" + str(st.session_state.reset_flag),
    )
    if libr != st.session_state.where["Library Type"]:
        if len(libr) > 0:
            st.session_state.where["Library Type"] = libr
        else:
            st.session_state.where["Library Type"] = None
        st.session_state.rerun_flag = True
