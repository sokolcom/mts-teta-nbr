import streamlit as st

import utils
import config as cfg


def config_tifu():
    """Configure TIFU KNN model"""
    
    params_tifu = dict()
    
    # задаем все гиперпараметры, кроме r (будем использовать предобработанный датасет)
    params_tifu['r'] = 0.75
    st.write('The parameter "r" is ', params_tifu['r'])
    
    params_tifu['k_nearest'] = st.number_input('The parameter "k_nearest" is', value=30)
    params_tifu['alpha'] = st.number_input('The parameter "alpha" is', value=0.95)
    params_tifu['top_k'] = st.number_input('The parameter "top_k" is', value=18)
    
    return params_tifu


def config_popular():
    """Configure Popularity-based model"""
    
    params_popular = dict()
    
    # задаем все гиперпараметры
    params_popular['top_k'] = st.number_input('The parameter "top_k" is', value=15)
    
    return params_popular


def pick_model():
    """Pick a custom (predefined) model"""
    with st.sidebar.expander("Model"):
        model_type = st.selectbox(
            "Choose a model",
            (
                cfg.MODEL_POPULAR,
                cfg.MODEL_TIFUKNN,
                # smth else?
            )
        )
        st.markdown("---")

        if model_type == cfg.MODEL_TIFUKNN:
            model_params = config_tifu()
        elif model_type == cfg.MODEL_POPULAR:
            model_params = config_popular()

    return model_type, model_params
