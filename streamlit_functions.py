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

import streamlit as st


def reset_all():
    st.session_state.where = {
        "First Category": None,
        "Second Category": None,
        "Package": None,
        "Manufacturer": None,
        "Library Type": None,
        "Stock": 1,
        "MFR.Part": None,
        "LCSC Part": None,
        "Description": None,
    }
    st.session_state.filter_data = {}
    st.session_state.sort_params = None
    st.session_state.price_qty = 100
    st.session_state.page = 1
    st.session_state.reset_flag = not st.session_state.reset_flag


def session_init():
    if st.session_state.get("page") is None:
        st.session_state.page = 1
    if st.session_state.get("where") is None:
        st.session_state.where = {
            "First Category": None,
            "Second Category": None,
            "Package": None,
            "Manufacturer": None,
            "Library Type": None,
            "Stock": 1,
            "MFR.Part": None,
            "LCSC Part": None,
            "Description": None,
        }
    if st.session_state.get("filter_data") is None:
        st.session_state.filter_data = {}
    if st.session_state.get("sort_params") is None:
        st.session_state.sort_params = None
    if st.session_state.get("price_qty") is None:
        st.session_state.price_qty = 100
    if st.session_state.get("rerun_flag") is None:
        st.session_state.rerun_flag = False
    if st.session_state.get("retrigger") is None:
        st.session_state.retrigger = False
    if st.session_state.get("reset_flag") is None:
        st.session_state.reset_flag = False
