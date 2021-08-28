import pandas as pd
import streamlit as st

import config as cfg
import utils
from models import pick_model
from train_model import train_tifu, train_popular


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

    model_type, model = pick_model()
        
    st.sidebar.markdown("---")

    st.sidebar.markdown(cfg.HTML_CREDITS, unsafe_allow_html=True)

    return model_type, model
        

def render_top(items_mapping, model_type):
    """Render top container (bcreate basket)"""
    items_title = [items_mapping[i]["title"] for i in list(items_mapping)]

    with st.container():
        
        layout = st.columns((2, 2))
        # айдишник клиента
        with layout[0].form(key="login"):
            login = st.text_input('Enter your login', value='0')
            btn_submit_login = st.form_submit_button(label="Sent")
        # новая корзина
        with layout[1].form(key="create_basket"):
            new_basket = st.multiselect("Select items", items_title, items_title[:cfg.DEFAULT_ITEMS_AMOUNT])
            btn_submit_basket = st.form_submit_button(label="Create basket")
            
        # отображение метрик для разных моделей
        layout = st.columns((2,1))
        if model_type == cfg.MODEL_TIFUKNN:
            metrics_gauge = utils.visualize_metrics(cfg.TIFU_METRICS)
            layout[0].plotly_chart(metrics_gauge, use_container_width=True)
        elif model_type == cfg.MODEL_POPULAR:
            metrics_gauge = utils.visualize_metrics(cfg.POPULAR_METRICS)
            layout[0].plotly_chart(metrics_gauge, use_container_width=True) 
        
    return login, new_basket


def render_mid(items_mapping, login, new_basket, model_type, model_params):
    """Render middle container (recommendations)"""

    with st.container():
        st.success('Hey, we highly recommend you...')
        
        if model_type == cfg.MODEL_TIFUKNN:
            items_ids = train_tifu(items_mapping,
                                   cfg.purchase_data,
                                   cfg.users_as_vectors,
                                   login,
                                   new_basket,
                                   model_params)
            
        elif model_type == cfg.MODEL_POPULAR:
            items_ids = train_popular(items_mapping,
                                      cfg.purchase_data,
                                      login,
                                      new_basket,
                                      model_params)
            
        recommendations = st.columns(cfg.ITEMS_PER_ROW)
        for i in range(min([cfg.ITEMS_PER_ROW, len(items_ids)])):
            recommendations[i].image(
                items_mapping[items_ids[i]]["img"],
                caption=items_mapping[items_ids[i]]["title"]
                )
            
        st.markdown("---")


def render_bot(items_mapping):
    """Render bottom container (item list)"""
    items_ids = list(items_mapping)

    st.markdown("### Items")
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


def render_body(model_type, model_params):
    """Render main body of the page (interactive form, items list)"""
    items_mapping = utils.get_items_mapping(cfg.ITEMS_MAPPING)

    welcome()
    login, new_basket = render_top(items_mapping, model_type)
    render_mid(items_mapping, login, new_basket, model_type, model_params)
    render_bot(items_mapping)


def render_page():
    """Render main page (sidebar + main body)"""
    model_type, model_params = render_sidebar()
    render_body(model_type, model_params)
