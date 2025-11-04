import streamlit as st
import requests
import numpy as np
import plotly.express as px

API_URL = "http://localhost:8000/analyze_prompt"

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
                st.success("Analysis Complete!")

                st.subheader("Variance")
                st.write(f"**Variance:** {result['variance']:.4f}")

                st.subheader("Closest to Average Output")
                st.info(result["average_output"])

                st.subheader("🔗 Pairwise Similarities Heatmap")
                sim_matrix = np.array(result["pairwise_similarities"])
                fig = px.imshow(
                    sim_matrix,
                    text_auto=False,
                    color_continuous_scale="Viridis",
                    title="Pairwise Cosine Similarities",
                    labels=dict(x="Output ID", y="Output ID", color="Similarity")
                )
                st.plotly_chart(fig, use_container_width=True)

                st.subheader("Explore Outputs")
                avg_sim = np.mean(sim_matrix, axis=1)
                points = [{"id": i, "avg_similarity": avg_sim[i]} for i in range(len(avg_sim))]

                fig2 = px.scatter(
                    points,
                    x="id",
                    y="avg_similarity",
                    title="Average Similarity of Each Output",
                    hover_data=["id"]
                )
                st.plotly_chart(fig2, use_container_width=True)

                st.markdown("Output Texts")
                selected_id = st.number_input(
                    "Select an Output ID to view:", min_value=0, max_value=len(result["outputs"]) - 1, value=0
                )
                selected_output = result["outputs"][selected_id]["text"]
                st.text_area(f"Output {selected_id}", value=selected_output, height=200)

