import pandas as pd
import numpy as np
import streamlit as st

import config as cfg
import utils
from models import pick_model


def config_page():
    """Configure page (page title, basic layout, etc)"""
    st.set_page_config(page_title="Team42 NBR Demo", layout='wide')


def welcome():
    #Render the main header
    st.markdown("# **Welcome to Team 42 Demo Stand :telescope:**")
    st.markdown("Here you can check out our `Next Basket Recommendations` and play around with it!")
    """st.markdown(
        
        * :bulb: Pick a model and set its hyper-parameters
        * :dizzy: Train it and check its performance metrics
        * :shopping_trolley: Create *your own* basket and get *your personal* recommedations
        -----
    
    )
"""

"""
def render_sidebar():
    #Render sidebar of the page
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
"""        


def render_workmode():
    workmode_dict={1: "Registered user: sign in and get recommendations", 2: "New user: you'll need firstly to create basket(s) "}
    def format_func(option):
        return workmode_dict[option]
    with st.container():
        workmode = st.selectbox("Firstly select a workmode: ", options = list(workmode_dict.keys()), format_func=format_func)
        st.markdown('And you will get recommendations!')
    st.write(f"You selected option {workmode} called ' {format_func(workmode)} '")    
    return workmode       

def render_top(items_mapping):
    #Render top container (create basket)
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

def render_userbase(items_mapping):
    """Render user base-based recommendation """
    with st.container():
        layout = st.columns((2, 3))
        recs = pd.read_csv(cfg.RECOM_BASE_TIFU_FULL)
        user_id_list = list(recs['user_id'])
        items_ids=[]
        with layout[0].form(key="Select your user id:"):       
            widget_user_id = st.selectbox("Select your user id:", user_id_list)
            btn_submit_id = st.form_submit_button(label="Recommend me a basket")   
            if btn_submit_id:
                st.write(f"Welcome, user {widget_user_id}!")
                items_ids_str = (recs['items'].loc[widget_user_id])
                items_frombase = items_ids_str.lstrip('[').rstrip(']').split(", ")
                #items_frombase = items_ids
                items_ids_bool =  [i in list(items_mapping) for i in items_frombase] #Choose just elements with pictures
                items_ids_int=np.array(items_frombase)[items_ids_bool]
                items_ids = list([str(i) for i in items_ids_int])
                #st.success(f"type(items_ids): {type(items_ids)}, \n items_ids: {items_ids},\n type(items_frombase): {type(items_frombase)}, len(items_frombase):{len(items_frombase)}, items_frombase: {items_frombase}, \n type(list(items_mapping)): {type(list(items_mapping))},list(items_mapping): {list(items_mapping)}, items_ids_bool: {items_ids_bool}")




        metrics_gauge = utils.visualize_metrics(cfg.STUB_METRICS)
        #layout[1].plotly_chart(metrics_gauge, use_container_width=True)
    return btn_submit_id, widget_user_id, items_ids

#def render_userbase_recom(items_ids):
    #####
    

def render_mid1(items_mapping, button):
    """Render middle1 container RECOMMENDATIONS"""  
     
    with st.container():
        #st.success('Hey, we do not know your preferences but we highly recommend you:')
        if button:
            st.success('Hey, now we know you and we can highly recommend you: (coming soon)')
            items_ids = list(items_mapping)
            #st.success(f"type: {type(items_ids)}, {items_ids}")
        else:
            st.success('Hey, we do not know your preferences yet but we highly recommend you:')
            items_ids = list(items_mapping)
            #st.success(f"type: {type(items_ids)}, {items_ids}")

        recom_size = min(cfg.ITEMS_PER_ROW, len(items_ids))    #avoid error if we are going to show a cart shorter than cfg.ITEMS_PER_ROW
        recommendations = st.columns(recom_size) #just how much columns
        for i in range(recom_size):
            recommendations[i].image(
                items_mapping[items_ids[i]]["img"],
                caption=items_mapping[items_ids[i]]["title"]
            )
        st.markdown("---")


def render_mid_userbase(items_mapping, button, items_frombase):
    """Render when you choose a user by id"""
    #at workmode 1 (registered user) button = btn_submit_id
    with st.container():
        if button:            
            st.success('Hey, we remember you and we can highly recommend you:')
            items_ids_bool =  [i in list(items_mapping) for i in items_frombase] #Choose just elements with pictures
            items_ids_int=np.array(items_frombase)[items_ids_bool]
            items_ids = list([str(i) for i in items_ids_int])
            #st.success(f"type(items_ids): {type(items_ids)}, \n items_ids: {items_ids},\n type(items_frombase): {type(items_frombase)}, len(items_frombase):{len(items_frombase)}, items_frombase: {items_frombase}, \n type(list(items_mapping)): {type(list(items_mapping))},list(items_mapping): {list(items_mapping)}, items_ids_bool: {items_ids_bool}")
        else:
            st.success('We do not know you and your preferences yet but we highly recommend you:')
            items_ids = list(items_mapping)
            #st.success(f"type: {type(items_ids)}, {items_ids}")
        recom_size = min(cfg.ITEMS_PER_ROW, len(items_ids))    #avoid error if we are going to show a cart shorter than cfg.ITEMS_PER_ROW
        recommendations = st.columns(recom_size) #just how much columns
        for i in range(recom_size):
            recommendations[i].image(
                items_mapping[items_ids[i]]["img"],
                caption=items_mapping[items_ids[i]]["title"]
            )
        st.markdown("---")


def render_LastBasket(items_mapping, btn_submit_basket,workmode):
    """Render middle2 container (last cart)"""
    items_ids = list(items_mapping)

    with st.container():
        if btn_submit_basket:
            st.success('Your last cart was:')
            recom_size = min(cfg.ITEMS_PER_ROW, len(items_ids))    #avoid error if we are going to show a cart shorter than cfg.ITEMS_PER_ROW
            recommendations = st.columns(recom_size) #just how much columns
            for i in range(recom_size):
                recommendations[i].image(
                    items_mapping[items_ids[i]]["img"],
                    caption=items_mapping[items_ids[i]]["title"]
                )
                      
        elif workmode ==2:
            st.success('Later you will see here your last cart ')
        else:
            st.success('Our most popular items: ')
        st.markdown("---")  


def render_bot(items_mapping):
    """Render bottom container (item catalogue)"""
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
    items_mapping_personal = utils.get_items_mapping(cfg.ITEMS_MAPPING)
    welcome()    
    workmode = render_workmode()

    if workmode ==2:
        btn_submit_basket, basket_bought = render_top(items_mapping)
        
        if btn_submit_basket:     
            items_mapping_personal = utils.itemtitle_to_itemdict(cfg.ITEMS_MAPPING, basket_bought) #Previous basket
        else:
            items_mapping_personal = utils.get_items_mapping(cfg.ITEMS_MAPPING)  #Common popularity Recommendations
        
        render_mid1 (items_mapping_personal, btn_submit_basket) #previous basket-based  Recommendations
        render_LastBasket (items_mapping_personal, btn_submit_basket, workmode) #
    else: # workmode ==1:    
        btn_submit_id, widget_user_id, items_ids = render_userbase(items_mapping)
        render_mid_userbase(items_mapping, btn_submit_id, items_ids)
        #render_mid2 (items_mapping, btn_submit_basket=0, workmode=workmode) #Common popularity Recommendations
    render_bot(items_mapping) #All items in the shop


def render_page():
    """Render main page (sidebar + main body)"""
    #render_sidebar()
    render_body()
