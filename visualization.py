import streamlit as st

def visualization_tab(triples):
    st.header("RDF Graph Visualization")

    # Show all triples in the graph
    if st.checkbox("Show all triples"):
        st.write("### Current RDF Triples in Graph:")
        for subj, pred, obj in triples:
            st.write(f"({subj}, {pred}, {obj})")

    # Download triples as Turtle format
    if st.button("Export as Turtle"):
        rdf_data = "\n".join([f"{s} {p} {o} ." for s, p, o in triples])
        st.download_button("Download RDF", rdf_data, file_name="ontology.ttl", mime="text/turtle")
