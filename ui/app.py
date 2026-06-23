import streamlit as st
from ui.client import ingest, query

st.title("Text to Graph")

tab1, tab2 = st.tabs(["Ingest Text", "Query Graph"])


with tab1:

    text = st.text_area("Enter text")

    if st.button("Build Graph"):

        result = ingest(text)

        st.write(result)


with tab2:

    question = st.text_input("Ask a question")

    if st.button("Ask"):

        result = query(question)

        st.write(result)