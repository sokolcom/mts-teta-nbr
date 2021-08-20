import pandas as pd
import streamlit as st

import config as cfg
from utils import get_items_mapping


def config_page():
    """Configure page (page title, basic layout, etc)"""
    st.set_page_config(page_title="Team42 NBR Demo", layout='wide')


def welcome():
    """Render the main header"""
    st.markdown("# **Welcome to Team 42 Demo Stand :telescope:**")
    st.markdown("Here you can check out our `Next Basket Recommendations` and play around with it!")
    st.markdown(
        """
        * :bulb: Pick a model and set its hyper-parameters
        * :dizzy: Train it and check its performance metrics
        * :shopping_trolley: Create *your own* basket and get *your personal* recommedations
        -----
    """
    )


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
        

def render_top(items_mapping, basket=[]):
    """Render top container (bcreate basket)"""
    items_title = [items_mapping[i]["title"] for i in list(items_mapping)]
    # basket = basket or items_title[:cfg.DEFAULT_ITEMS_AMOUNT]

    with st.container():
        layout = st.columns((2, 3))
        with layout[0].form(key="create_basket"):
            widget_basket = st.multiselect("Select items", items_title, items_title[:cfg.DEFAULT_ITEMS_AMOUNT])
            btn_submit_basket = st.form_submit_button(label="Create basket")

        # figure = [1, 2, 3]
        # layout[1].plot_placeholder.plotly_chart(figure, use_container_width=True)


def render_mid(items_mapping):
    """Render middle container (recommendations)"""
    items_ids = list(items_mapping)

    with st.container():
        st.success('Hey, we highly recommend you...')

        recommendations = st.columns(cfg.ITEMS_PER_ROW)
        for i in range(cfg.ITEMS_PER_ROW):
            recommendations[i].image(
                items_mapping[items_ids[i]]["img"],
                caption=items_mapping[items_ids[i]]["title"]
            )
        st.markdown("---")


def render_bot(items_mapping, basket=[]):
    """Render bottom container (item list)"""
    items_ids = list(items_mapping)

    st.markdown("### Items")
    with st.container():
        items = st.columns(cfg.ITEMS_PER_ROW)

        for i in range(cfg.ITEMS_AMOUNT):
            with items[i % cfg.ITEMS_PER_ROW].container():
                st.image(
                    items_mapping[items_ids[i]]["img"],
                    caption=items_mapping[items_ids[i]]["title"]
                )
                # st.number_input("Qty", min_value=0, value=0, step=1)
                # btn_add_item = st.form_submit_button(label="Add to basket")
                st.markdown("---")



def render_body():
    """Render main body of the page (interactive form, items list)"""
    items_mapping = get_items_mapping(cfg.ITEMS_MAPPING)

    welcome()
    render_top(items_mapping)
    render_mid(items_mapping)
    render_bot(items_mapping)


def render_page():
    """Render main page (sidebar + main body)"""
    render_sidebar()
    render_body()
