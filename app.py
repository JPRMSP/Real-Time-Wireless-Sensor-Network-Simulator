# app.py
import streamlit as st
import numpy as np
import networkx as nx
import plotly.graph_objects as go
import time

st.set_page_config(page_title="Real-Time Sensor Network Simulator", layout="wide")
st.title("📡 Real-Time Wireless Sensor Network Simulator")

# Parameters
num_sensors = st.sidebar.slider("Number of Sensors", 5, 50, 15)
num_objects = st.sidebar.slider("Number of Moving Objects", 1, 10, 3)
field_size = 100

# Initialize sensor nodes
np.random.seed(42)
sensors = {
    i: {
        "pos": np.random.rand(2) * field_size,
        "energy": 100,
        "data": 0
    } for i in range(num_sensors)
}

# Initialize objects
objects = {
    i: {
        "pos": np.random.rand(2) * field_size,
        "vel": (np.random.rand(2) - 0.5) * 2
    } for i in range(num_objects)
}

# Energy-aware routing function (simplified)
def update_energy(sensor_id):
    sensors[sensor_id]["energy"] -= 0.1
    sensors[sensor_id]["data"] = np.random.randint(20, 100)
    return sensors[sensor_id]["energy"]

# Plot function
def plot_network():
    fig = go.Figure()
    # Sensors
    for sid, s in sensors.items():
        fig.add_trace(go.Scatter(x=[s["pos"][0]], y=[s["pos"][1]],
                                 mode='markers+text',
                                 marker=dict(size=12, color=s["energy"], colorscale='Viridis', showscale=True),
                                 text=[f"S{sid}"],
                                 textposition="top center"))
    # Objects
    for oid, o in objects.items():
        fig.add_trace(go.Scatter(x=[o["pos"][0]], y=[o["pos"][1]],
                                 mode='markers+text',
                                 marker=dict(size=15, symbol='x', color='red'),
                                 text=[f"O{oid}"], textposition="bottom center"))
    fig.update_layout(xaxis=dict(range=[0, field_size]), yaxis=dict(range=[0, field_size]),
                      width=800, height=600, title="Sensor Network Field")
    return fig

# Simulation loop
run_sim = st.button("Start Simulation")
if run_sim:
    placeholder = st.empty()
    for t in range(100):
        # Move objects
        for o in objects.values():
            o["pos"] += o["vel"]
            o["pos"] = np.clip(o["pos"], 0, field_size)
        # Update sensor readings
        for sid in sensors.keys():
            update_energy(sid)
        placeholder.plotly_chart(plot_network(), use_container_width=True)
        time.sleep(0.3)
