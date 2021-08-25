import streamlit as st


import config as cfg


def config_tifu():
    """Configure TIFU KNN model"""
    st.radio("blah", ["blah", "blah-blah", "blah-blah-blah"])
    return None


def config_popular():
    """Configure Popularity-based model"""
    st.radio("Sheeeesh", ["yes", "yessir", "yessirski"])
    return None


def pick_model():
    """Pick a custom (predefined) model"""
    with st.sidebar.expander("Model"):
        model_type = st.selectbox(
            "Choose a model",
            (
                cfg.MODEL_TIFUKNN,
                cfg.MODEL_POPULAR,
                # smth else?
            )
        )
        st.markdown("---")

        if model_type == cfg.MODEL_TIFUKNN:
            model = config_tifu()
        elif model_type == cfg.MODEL_POPULAR:
            model = config_popular()

    return model
