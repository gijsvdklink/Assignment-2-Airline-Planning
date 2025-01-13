import pandas as pd
import networkx as nx
import plotly.graph_objects as go

# Step 1: Load the data
file_path = "FlightTimes_FRA.csv"
data = pd.read_csv(file_path, index_col=0)  # Use the first column as the index

# Filter for only FRA, AMS, MUC, and CDG
filtered_airports = ["FRA", "AMS", "MUC", "CDG"]
flight_times = data.loc[filtered_airports, "Small Freighter"]

# Step 2: Define time intervals (up to 400 minutes)
time_intervals = [i * 6 for i in range(int(400 / 6) + 1)]  # Every 6 minutes up to 400 minutes

# Step 3: Create the graph
G = nx.DiGraph()

# Reverse airport order for proper placement (FRA at the top)
reversed_airports = list(reversed(filtered_airports))

# Add nodes for FRA and other airports at each time interval
for airport in filtered_airports:
    for t in time_intervals:
        G.add_node((airport, t), pos=(t, reversed_airports.index(airport)))  # Use reversed index

# Add edges for flights that start and return to FRA
for airport in filtered_airports:
    if airport != "FRA":
        flight_time = flight_times[airport]
        for t in time_intervals:
            # Outbound flight from FRA to another airport
            if t + flight_time in time_intervals and t + 2 * flight_time <= 400:
                G.add_edge(("FRA", t), (airport, t + flight_time))
                # Return flight from the airport back to FRA
                G.add_edge((airport, t + flight_time), ("FRA", t + 2 * flight_time))

# Add ground arcs
for airport in filtered_airports:
    for t in time_intervals:
        # FRA has unlimited ground arcs
        if airport == "FRA":
            if t + 6 in time_intervals:  # Add ground arc every 6 minutes
                G.add_edge((airport, t), (airport, t + 6))
        else:
            # Check conditions for non-FRA airports
            incoming_exists = any(edge[1] == (airport, t) for edge in G.edges)
            outgoing_exists_after_t = any(
                edge[0] == (airport, t2) for t2 in time_intervals if t2 > t for edge in G.edges
            )
            if incoming_exists and outgoing_exists_after_t and t + 6 in time_intervals:
                G.add_edge((airport, t), (airport, t + 6))

# Step 4: Remove nodes with no edges
nodes_to_remove = [node for node in G.nodes if G.degree(node) == 0]
G.remove_nodes_from(nodes_to_remove)

# Step 5: Dynamic Programming Initialization
dp = {}  # Store the minimum cost for each node
parent = {}  # Store the parent node for reconstructing the path

# Initialize DP table
for node in G.nodes:
    dp[node] = float('inf')  # Initialize all costs to infinity
    parent[node] = None

# Set the cost of the end node (e.g., ("FRA", 400)) to 0
end_node = ("FRA", 400)
dp[end_node] = 0

# Step 6: Backward DP Computation
for time in range(400, -1, -6):  # Iterate backward in time
    for node in [n for n in G.nodes if n[1] == time]:  # Get nodes at the current time
        for pred in G.predecessors(node):  # Check all predecessors of the current node
            cost = dp[node] + G[pred][node]['weight']  # Update cost
            if cost < dp[pred]:  # Keep the minimum cost
                dp[pred] = cost
                parent[pred] = node

# Step 7: Reconstruct the Shortest Path
start_node = ("FRA", 0)
current_node = start_node
shortest_path = []

while current_node is not None:
    shortest_path.append(current_node)
    current_node = parent[current_node]

print("Shortest Path:", shortest_path)

# Step 8: Extract positions for plotting
pos = nx.get_node_attributes(G, "pos")
edges = list(G.edges)

# Step 9: Visualize the graph with shortest path highlighted
edge_x = []
edge_y = []
shortest_path_edges = list(zip(shortest_path, shortest_path[1:]))

for edge in G.edges:
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x.append(x0)
    edge_x.append(x1)
    edge_x.append(None)
    edge_y.append(y0)
    edge_y.append(y1)
    edge_y.append(None)

edge_trace = go.Scatter(
    x=edge_x,
    y=edge_y,
    line=dict(width=0.5, color="#888"),
    hoverinfo="none",
    mode="lines",
)

# Highlight the shortest path
shortest_edge_x = []
shortest_edge_y = []
for edge in shortest_path_edges:
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    shortest_edge_x.append(x0)
    shortest_edge_x.append(x1)
    shortest_edge_x.append(None)
    shortest_edge_y.append(y0)
    shortest_edge_y.append(x1)
    shortest_edge_y.append(None)

shortest_edge_trace = go.Scatter(
    x=shortest_edge_x,
    y=shortest_edge_y,
    line=dict(width=2, color="red"),
    hoverinfo="none",
    mode="lines",
)

node_x = []
node_y = []
node_text = []
for node, p in pos.items():
    node_x.append(p[0])
    node_y.append(p[1])
    node_text.append(f"{node[0]} @ {node[1]} min")

node_trace = go.Scatter(
    x=node_x,
    y=node_y,
    mode="markers",
    hoverinfo="text",
    marker=dict(size=5, color="blue"),
    text=node_text,
)

fig = go.Figure(data=[edge_trace, shortest_edge_trace, node_trace])
fig.update_layout(
    title="Time-Space Graph with Demand-Based Shortest Path (Dynamic Programming)",
    title_x=0.5,
    xaxis=dict(title="Time (minutes)", range=[0, 400], showgrid=True),
    yaxis=dict(
        title="Airports",
        tickmode="array",
        tickvals=list(range(len(reversed_airports))),  # Tick positions match reversed order
        ticktext=reversed_airports,  # Tick labels are in reversed order
    ),
    showlegend=False,
    hovermode="closest",
    height=800,
    width=1200,
)

fig.show()
