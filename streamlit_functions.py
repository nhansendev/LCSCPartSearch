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
