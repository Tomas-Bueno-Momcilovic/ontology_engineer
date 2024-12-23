import streamlit as st
from utils import get_full_uri, add_triple

def triple_creation_tab(namespaces, triples):
    st.header("Create RDF Triples with Prefixes")

    # Adjust the width of columns
    col1, col2, col3, col4, col5, col6 = st.columns([1, 3, 1, 3, 1, 3])

    # Subject section
    with col1:
        subject_prefix = st.selectbox("Prefix", options=list(namespaces.keys()), key="subject_prefix_select")
    with col2:
        subject_local = st.text_input("Local Part", key="subject_local_input")

    # Predicate section
    with col3:
        predicate_prefix = st.selectbox("Prefix", options=list(namespaces.keys()), key="predicate_prefix_select")
    with col4:
        predicate_local = st.text_input("Local Part", key="predicate_local_input")

    # Object section
    with col5:
        object_prefix = st.selectbox("Prefix", options=list(namespaces.keys()), key="object_prefix_select")
    with col6:
        object_local = st.text_input("Local Part", key="object_local_input")
        is_literal = st.checkbox("Is Object a Literal?", value=False)

    # Add triple logic
    if st.button("Add Triple", key="add_triple_button"):
        try:
            subject_full = get_full_uri(subject_prefix, subject_local, namespaces)
            predicate_full = get_full_uri(predicate_prefix, predicate_local, namespaces)

            if is_literal:
                object_full = object_local
            else:
                object_full = get_full_uri(object_prefix, object_local, namespaces)

            triple = (subject_full, predicate_full, object_full)
            triples.append(triple)
            st.success(f"Triple added: {triple}")
        except Exception as e:
            st.error(f"Error: {e}")
