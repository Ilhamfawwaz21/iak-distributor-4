import pandas as pd
from graph_routes import create_graph, find_cheapest_route, find_fastest_route

def process_purchases(df_graph, df_purchases):
    G = create_graph(df_graph)
    
    results = []

    for index, row in df_purchases.iterrows():
        try:
            id_log = row['id_log']
            kota_asal = row['kota_asal'].lower()
            kota_tujuan = row['kota_tujuan'].lower()
            berat = float(row['berat'])  # Convert to float

            if kota_asal not in G or kota_tujuan not in G:
                raise ValueError(f"Kota asal atau tujuan tidak ditemukan: {kota_asal} - {kota_tujuan}")

            # Menemukan rute terendah biaya
            cheapest_path, total_cost = find_cheapest_route(G, kota_asal, kota_tujuan, berat)

            # Menemukan rute tercepat
            fastest_path, total_time = find_fastest_route(G, kota_asal, kota_tujuan)

            results.append({
                'id_log': id_log,
                'kota_asal': kota_asal,
                'kota_tujuan': kota_tujuan,
                'berat': berat,
                'total_biaya': f"Rp{total_cost:,.0f}" if total_cost < float('infinity') else 'Tidak Ditemukan',
                'total_waktu': f"{total_time:.2f} jam" if total_time < float('infinity') else 'Tidak Ditemukan'
            })
        except Exception as e:
            results.append({
                'id_log': row.get('id_log', 'Unknown'),
                'error': str(e)
            })

    return pd.DataFrame(results)