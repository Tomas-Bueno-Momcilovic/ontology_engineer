import streamlit as st
from utils import COMMON_NAMESPACES

def configuration_tab(namespaces):
    st.header("Namespace Configuration")

    # Display current namespaces
    st.write("### Current Namespaces")
    for prefix, uri in namespaces.items():
        if prefix in COMMON_NAMESPACES:
            st.write(f"**{prefix}:** {uri} (common namespace)")
        else:
            st.write(f"**{prefix}:** {uri}")

    # Input fields for adding a new namespace
    st.write("### Add a New Namespace")
    new_prefix = st.text_input("Prefix", "")
    new_uri = st.text_input("Namespace URI", "")

    if st.button("Add Namespace"):
        if new_prefix and new_uri:
            if new_prefix in COMMON_NAMESPACES:
                st.error(f"Cannot modify common namespace '{new_prefix}'.")
            else:
                namespaces[new_prefix] = new_uri
                st.success(f"Namespace '{new_prefix}' added.")
        else:
            st.error("Both fields must be filled out to add a namespace.")
