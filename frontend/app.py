import streamlit as st
import requests
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from streamlit_plotly_events import plotly_events

API_URL = "http://localhost:8000/analyze_prompt"

if "result" not in st.session_state:
    st.session_state["result"] = None
if "analysis_done" not in st.session_state:
    st.session_state["analysis_done"] = False

st.set_page_config(page_title="Semantic FingerPrinter", layout="wide")

st.title("Semantic FingerPrinter Frontend")
st.markdown("""
this tool analyzes the variance and semantic similarity between multiple 
LLM outputs, enter a prompt, and/or plan, along with a specified number of 
outputs (n) to generate.     
""")

with st.sidebar:
    st.header("Input Parameters")
    prompt = st.text_area("System Prompt", height=150, placeholder="Enter the System Prompt here...")
    #not MVP #plan = st.text_area("Plan", height=150, placeholder="Enter Plan Name here...")
    n = st.number_input("Number of Outputs (n)", min_value = 2, max_value = 1000, value = 10)
    #not MVP #uploaded_doc = st.file_uploader("Optional Docuement", type=["txt", "pdf", "docx"])
    submit = st.button("Run Analysis")

if submit:
    if not prompt:
        st.warning("Please enter a prompt before running the analysis.")
    else:
        with st.spinner("Analyzing outputs... this may take a few moments"):
            #files = None
            #if uploaded_doc is not None:
            #    files = {"document": uploaded_doc.getvalue()}

            payload = {
                "prompt": prompt,
                "n": n
            }

            response = requests.post(API_URL, json=payload)

            if response.status_code != 200:
                st.error(f"API ERROR: {response.status_code} - {response.text}")
            else:
                result = response.json()
                st.session_state["result"] = result
                st.session_state["analysis_done"] = True

if st.session_state.get("analysis_done"):
    result = st.session_state["result"]
    st.success("Analysis Complete!")

    st.subheader("Variance")
    st.write(f"**Variance:** {result['variance']:.4f}")

    st.subheader("Closest to Average Output")
    st.info(result["average_output"])

    # Define sim_matrix early since it's used in multiple places
    sim_matrix = np.array(result["pairwise_similarities"])

    st.subheader("Explore Outputs")
    avg_sim = np.mean(sim_matrix, axis=1)
    
    # Create figure using graph_objects
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=list(range(len(avg_sim))),
        y=avg_sim.tolist(),
        mode='markers',
        marker=dict(size=10),
        hovertemplate='Output ID: %{x}<br>Avg Similarity: %{y:.4f}<extra></extra>'
    ))
    
    fig2.update_layout(
        title="Average Similarity of Each Output",
        xaxis_title="Output ID",
        yaxis_title="Average Similarity",
        hovermode='closest'
    )
    
    st.markdown("**Click on a point to view that output below:**")
    
    # --- Handle interactive selection ---
    selected_points = plotly_events(
        fig2,
        click_event=True,
        hover_event=False,
        select_event=False,
        key="scatter_click"
    )
    
    # If a point was clicked, show the selected output
    if selected_points:
        clicked_id = int(selected_points[0]["x"])
        
        # Show output text
        clicked_output = result["outputs"][clicked_id]["text"]
        st.markdown(f"Output {clicked_id} (Selected)")
        st.text_area(f"Output {clicked_id}", value=clicked_output, height=200, key=f"output_{clicked_id}")
    
    else:
        st.markdown("Output Texts")
        selected_id = st.number_input(
            "Or select manually:",
            min_value=0,
            max_value=len(result["outputs"]) - 1,
            value=0
        )
        selected_output = result["outputs"][selected_id]["text"]
        st.text_area(f"Output {selected_id}", value=selected_output, height=200, key=f"manual_output_{selected_id}")

    st.subheader("Pairwise Similarities Heatmap")
    fig = px.imshow(
        sim_matrix,
        text_auto=False,
        color_continuous_scale="Viridis",
        title="Pairwise Cosine Similarities",
        labels=dict(x="Output ID", y="Output ID", color="Similarity")
    )
    st.plotly_chart(fig, use_container_width=True)