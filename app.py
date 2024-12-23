import streamlit as st
from config import configuration_tab
from triple_creation import triple_creation_tab
from visualization import visualization_tab
from utils import load_data, save_data

# Set the app to wide mode at the very beginning
st.set_page_config(layout="wide")

# Ensure namespaces and triples are stored in session state
if "namespaces" not in st.session_state:
    st.session_state.namespaces, st.session_state.triples = load_data()

def main():
    st.title("Ontology Engineering Assistant")

    # Create a sidebar for file operations
    st.sidebar.header("File Operations")
    selected_option = st.sidebar.selectbox("Select Operation", ["Load Saved Data", "Create New Data"])

    # Handle loading saved data
    if selected_option == "Load Saved Data":
        file = st.sidebar.file_uploader("Upload your saved data", type=["json", "ttl"])
        if file:
            st.session_state.namespaces, st.session_state.triples = load_data(file)
            st.sidebar.success("Data loaded successfully.")
    
    # Handle creating new data
    elif selected_option == "Create New Data":
        if st.sidebar.button("Start Fresh"):
            st.session_state.namespaces, st.session_state.triples = load_data()  # Reset to common namespaces

    # Create tabs for configuration, triple creation, and visualization
    tabs = st.tabs(["Configuration", "Triple Creation", "Visualization"])

    # Tab 1: Namespace Configuration
    with tabs[0]:
        configuration_tab(st.session_state.namespaces)

    # Tab 2: Triple Creation
    with tabs[1]:
        triple_creation_tab(st.session_state.namespaces, st.session_state.triples)

    # Tab 3: RDF Graph Visualization
    with tabs[2]:
        visualization_tab(st.session_state.triples)

    # Save data to a file
    if st.sidebar.button("Save Data"):
        save_data(st.session_state.namespaces, st.session_state.triples)
        st.sidebar.success("Data saved successfully.")

if __name__ == "__main__":
    main()
