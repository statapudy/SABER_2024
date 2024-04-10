import streamlit as st

def app():
    with st.sidebar:
        with st.expander("Expander Title"):
            st.write("This is the content inside the expander.")

if __name__ == "__main__":
    app()