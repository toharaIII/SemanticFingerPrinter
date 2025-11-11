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

    st.subheader("Variance Between Individual Outputs")
    st.write(f"**Variance:** {result['variance']:.4f}")

    st.subheader("Closest to Average Output")
    st.info(result["average_output"])

    sim_matrix = np.array(result["pairwise_similarities"])

    st.subheader("Explore Outputs")
    centroid_sim = np.array(result["centroid_similarities"])
    
    # Calculate statistics for overlays
    median_sim = np.median(centroid_sim)
    mean_sim = np.mean(centroid_sim)
    q1_sim = np.percentile(centroid_sim, 25)
    q3_sim = np.percentile(centroid_sim, 75)
    
    # Create beeswarm effect by adding small random jitter to x-coordinates
    np.random.seed(42)  # For reproducibility
    jitter_amount = 0.02
    x_jittered = np.random.uniform(-jitter_amount, jitter_amount, len(centroid_sim))
    
    # Debug output
    st.write(f"Debug - Number of points: {len(centroid_sim)}, Values: {centroid_sim}")
    
    # Create figure with beeswarm plot
    fig2 = go.Figure()
    
    # Add the beeswarm points
    fig2.add_trace(go.Scatter(
        x=x_jittered,
        y=centroid_sim.tolist(),
        mode='markers',
        marker=dict(
            size=12,
            color='#636EFA',
            opacity=0.7,
            line=dict(width=1, color='white')
        ),
        customdata=list(range(len(centroid_sim))),
        hovertemplate='Output ID: %{customdata}<br>Similarity to Centroid: %{y:.4f}<extra></extra>',
        name='Outputs',
        showlegend=False
    ))

        # Add median line
    fig2.add_shape(
        type="line",
        x0=-0.5, x1=0.5,
        y0=median_sim, y1=median_sim,
        line=dict(color="red", width=2, dash="solid"),
    )
    fig2.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='lines',
        line=dict(color='red', width=2),
        name=f'Median: {median_sim:.4f}',
        showlegend=True
    ))
    
    # Add mean line
    fig2.add_shape(
        type="line",
        x0=-0.5, x1=0.5,
        y0=mean_sim, y1=mean_sim,
        line=dict(color="orange", width=2, dash="dash"),
    )
    fig2.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='lines',
        line=dict(color='orange', width=2, dash='dash'),
        name=f'Mean: {mean_sim:.4f}',
        showlegend=True
    ))
    
    # Add Q1 line
    fig2.add_shape(
        type="line",
        x0=-0.5, x1=0.5,
        y0=q1_sim, y1=q1_sim,
        line=dict(color="gray", width=1.5, dash="dot"),
    )
    fig2.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='lines',
        line=dict(color='gray', width=1.5, dash='dot'),
        name=f'Q1: {q1_sim:.4f}',
        showlegend=True
    ))
    
    # Add Q3 line
    fig2.add_shape(
        type="line",
        x0=-0.5, x1=0.5,
        y0=q3_sim, y1=q3_sim,
        line=dict(color="gray", width=1.5, dash="dot"),
    )
    fig2.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='lines',
        line=dict(color='gray', width=1.5, dash='dot'),
        name=f'Q3: {q3_sim:.4f}',
        showlegend=True
    ))
    
    # Add subtle IQR box
    fig2.add_shape(
        type="rect",
        x0=-0.5, x1=0.5,
        y0=q1_sim, y1=q3_sim,
        fillcolor="lightgray",
        opacity=0.15,
        line=dict(width=0),
        layer="below"
    )


    fig2.update_layout(
        title="Similarity to Centroid Distribution",
        xaxis_title="",
        yaxis_title="Cosine Similarity to Centroid",
        #hovermode='closest',
        xaxis=dict(
            showgrid=False,
            showticklabels=False,
            range=[-0.1, 0.1]
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='lightgray'
        ),
        height=500,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99
        )
    )
    
    st.markdown("**Click on a point to view that output below:**")
    
    # --- Handle interactive selection ---
    selected_points = st.plotly_chart(
    fig2,
    use_container_width=True,
    on_select="rerun",
    selection_mode="points",
    key="scatter_click"
    )
    
    st.write("Selected points:", selected_points)


    # If a point was clicked, show the selected output
    if selected_points and selected_points.get("selection") and selected_points["selection"].get("points"):
        clicked_id = selected_points["selection"]["points"][0]["point_index"]
        
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