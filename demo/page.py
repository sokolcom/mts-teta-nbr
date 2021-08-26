import pandas as pd
import streamlit as st

import config as cfg
import utils
from models import pick_model


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

    model = pick_model()
    st.sidebar.markdown("---")

    st.sidebar.markdown(cfg.HTML_CREDITS, unsafe_allow_html=True)

    return model
        

def render_top(items_mapping):
    """Render top container (create basket)"""
    items_title = [items_mapping[i]["title"] for i in list(items_mapping)]

    with st.container():
        layout = st.columns((2, 3))
        with layout[0].form(key="create_basket"):
            widget_basket = st.multiselect("Select items", items_title, items_title[:cfg.DEFAULT_ITEMS_AMOUNT])
            btn_submit_basket = st.form_submit_button(label="Create basket")
            if btn_submit_basket:
                basket_bought = widget_basket
            else:
                basket_bought = []
        
            #if btn_submit_basket:
        metrics_gauge = utils.visualize_metrics(cfg.STUB_METRICS)
        layout[1].plotly_chart(metrics_gauge, use_container_width=True)
        return btn_submit_basket, basket_bought

def render_mid1(items_mapping, btn_submit_basket):
    """Render middle container (recommendations)"""
    items_ids = list(items_mapping)

    with st.container():

        #st.success('Hey, we do not know your preferences but we highly recommend you:')
        if btn_submit_basket:
            st.success('Hey, we know you and we can highly recommend you: (coming soon)')
        else:
            st.success('Hey, we do not know your preferences but we highly recommend you:')

        recom_size = min(cfg.ITEMS_PER_ROW, len(items_ids))    #avoid error if we are going to show a cart shorter than cfg.ITEMS_PER_ROW
        recommendations = st.columns(recom_size) #just how much columns
        for i in range(recom_size):
            recommendations[i].image(
                items_mapping[items_ids[i]]["img"],
                caption=items_mapping[items_ids[i]]["title"]
            )
        st.markdown("---")


def render_mid2(items_mapping, btn_submit_basket):
    """Render middle container (recommendations)"""
    items_ids = list(items_mapping)

    with st.container():

        if btn_submit_basket:
            st.success('Your last cart was:')
        else:
            st.success('Later you will see here your last cart, but first have a look again on our most popular items: ')
        recom_size = min(cfg.ITEMS_PER_ROW, len(items_ids))    #avoid error if we are going to show a cart shorter than cfg.ITEMS_PER_ROW
        recommendations = st.columns(recom_size) #just how much columns
        for i in range(recom_size):
            recommendations[i].image(
                items_mapping[items_ids[i]]["img"],
                caption=items_mapping[items_ids[i]]["title"]
            )
        st.markdown("---")


def render_bot(items_mapping):
    """Render bottom container (item list)"""
    items_ids = list(items_mapping)

    st.markdown("### Items catalogue")
    with st.container():
        items = st.columns(cfg.ITEMS_PER_ROW)

        for i in range(cfg.ITEMS_AMOUNT):
            with items[i % cfg.ITEMS_PER_ROW].container():
                st.image(
                    items_mapping[items_ids[i]]["img"],
                    caption=items_mapping[items_ids[i]]["title"],
                    width=cfg.ITEM_IMG_WIDTH
                )
                st.markdown("---")


def render_body():
    """Render main body of the page (interactive form, items list)"""
    items_mapping = utils.get_items_mapping(cfg.ITEMS_MAPPING)


    welcome()
    btn_submit_basket, basket_bought = render_top(items_mapping)
    items_mapping_personal = utils.get_items_mapping(cfg.ITEMS_MAPPING)
    if btn_submit_basket:
        #items_mapping_personal = utils.get_items_mapping(cfg.ITEMS_MAPPING_TIFU)        
        items_mapping_personal = utils.itemtitle_to_itemdict(cfg.ITEMS_MAPPING, basket_bought)
    else:
        items_mapping_personal = utils.get_items_mapping(cfg.ITEMS_MAPPING)
    render_mid1 (items_mapping_personal, btn_submit_basket) #Recommendations
    render_mid2 (items_mapping_personal, btn_submit_basket) #Recommendations
    render_bot(items_mapping) #All items in the shop


def render_page():
    """Render main page (sidebar + main body)"""
    render_sidebar()
    render_body()
