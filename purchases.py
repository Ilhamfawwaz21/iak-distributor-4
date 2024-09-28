import pandas as pd
from graph_routes import create_graph, find_cheapest_route, find_fastest_route

def process_purchases(df_graph, df_purchases):
    G = create_graph(df_graph)
    
    results = pd.DataFrame(columns=['id_log','id_pembelian', 'total_biaya', 'total_waktu'])

    for index, row in df_purchases.iterrows():
        id_log = row['id_log']
        id_pembelian = row['id_pembelian']
        kota_asal = row['kota_asal'].lower()
        kota_tujuan = row['kota_tujuan'].lower()
        berat = row['berat']

        # Menemukan rute terendah biaya
        cheapest_path, total_cost = find_cheapest_route(G, kota_asal, kota_tujuan, berat)

        # Menemukan rute tercepat
        fastest_path, total_time = find_fastest_route(G, kota_asal, kota_tujuan)

        # Menambahkan hasil ke DataFrame
        results.loc[len(results)] = {
            'id_log': id_log,
            'id_pembelian': id_pembelian,
            'total_biaya': f"Rp{total_cost:,.0f}" if total_cost < float('infinity') else 'Tidak Ditemukan',
            'total_waktu': f"{total_time:.2f} jam" if total_time < float('infinity') else 'Tidak Ditemukan'
        }

    return results