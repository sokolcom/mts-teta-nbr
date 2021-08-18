import pandas as pd
import streamlit as st

import config as cfg


def config_page():
    """Configure page (page title, basic layout, etc)"""
    st.set_page_config(page_title="Team42 NBR Demo", layout='wide')


def render_sidebar():
    """Render sidebar of the page"""
    st.sidebar.markdown("# :avocado: Team 42 :avocado:")
    st.sidebar.markdown("### Next Basket Recommendation")
    st.sidebar.markdown("---")

    with st.sidebar.expander("About"):
        st.markdown(cfg.DESCRIPTION)
    st.sidebar.markdown("---")

    st.sidebar.radio("Algorithm:", ["TIFU KNN", "Apriori", "Popularity-based"])
    st.sidebar.markdown("---")

    st.sidebar.button("Visualization?")
    st.sidebar.markdown("---")

    st.sidebar.markdown(cfg.HTML_CREDITS, unsafe_allow_html=True)
        


def render_body():
    """Render main body of the page (interactive form, items list)"""
    df = pd.read_csv(cfg.DATA_PATH)

    # Top container
    with st.container():
        layout = st.columns([2, 3])

        with layout[0].form(key="create_basket"):
            st.multiselect("Select items", list(df["from"]), df["from"][:cfg.DEFAULT_ITEMS_AMOUNT])  # TODO labels
            submit_button = st.form_submit_button(label="Create basket")

        layout[1].success('Hey, we highly recommend you...')


    # Bottom container
    st.markdown("### Items")
    with st.container():
        items = st.columns(cfg.ITEMS_PER_ROW)

        for i in range(cfg.ITEMS_AMOUNT):
            with items[i % cfg.ITEMS_PER_ROW].form(key=f"item_{i}"):
                st.image(cfg.RAND_IMAGE, caption=f"ITEM #{i + 1}")
                submit_button = st.form_submit_button(label="Add to basket")


def render_page():
    """Render main page (sidebar + main body)"""
    render_sidebar()
    render_body()