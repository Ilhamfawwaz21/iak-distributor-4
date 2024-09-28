import networkx as nx

rate_per_km = 20
rate_per_kg = 15000
speed_darat = 80
asuransi = 0.03

def create_graph(df_graph):
    G = nx.Graph()
    for index, row in df_graph.iterrows():
        source = row['source'].lower()
        destination = row['destination'].lower()
        distance = row['weight']
        time = distance / speed_darat  # Estimasi waktu tiba
        G.add_edge(source, destination, distance=distance, time=time)
    return G

def find_cheapest_route(G, start, end, weight):
    try:
        def cost_func(u, v, data):
            distance = data['distance']
            cost1 = (distance * rate_per_km) + (weight * rate_per_kg)
            cost = cost1 + (asuransi * cost1)
            return cost

        path = nx.dijkstra_path(G, source=start, target=end, weight=cost_func)
        total_cost = 0
        for i in range(len(path)-1):
            u = path[i]
            v = path[i+1]
            edge_data = G.get_edge_data(u, v)
            distance = edge_data['distance']
            cost1 = (distance * rate_per_km) + (weight * rate_per_kg)
            cost = cost1 + (asuransi * cost1)
            total_cost += cost
        return path, total_cost
    except nx.NetworkXNoPath:
        return None, float('infinity')

def find_fastest_route(G, start, end):
    try:
        path = nx.dijkstra_path(G, source=start, target=end, weight='time')
        total_time = nx.dijkstra_path_length(G, source=start, target=end, weight='time')
        return path, total_time
    except nx.NetworkXNoPath:
        return None, float('infinity')