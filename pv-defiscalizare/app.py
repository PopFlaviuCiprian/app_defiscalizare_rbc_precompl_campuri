from flask import Flask, render_template, request, jsonify
import pandas as pd
import webbrowser
from threading import Timer
import os
import signal

app = Flask(__name__)

# Citirea fișierului Excel
file_path = "clienti.xlsx"
df = pd.read_excel(file_path, sheet_name="Sheet1")

def get_unique_clients():
    return df[["Nume_Companie", "Cod_Fiscal", "Aviz_Distributie", "Marca", "Model"]].drop_duplicates().to_dict("records")

def get_addresses_by_client(client_name):
    return df[df["Nume_Companie"] == client_name]["Adresa_Punct_Lucru"].unique().tolist()

@app.route('/')
def pv_defiscalizare():
    clients = get_unique_clients()
    return render_template("pv_defiscalizare.html", clients=clients)

@app.route('/get_client_data', methods=['GET'])
def get_client_data():
    client_name = request.args.get('q')

    # Verificăm dacă clientul există
    client_rows = df[df['Nume_Companie'] == client_name]
    if client_rows.empty:
        return jsonify({'error': 'Clientul nu a fost găsit'}), 404

    client_data = client_rows.iloc[0]
    addresses = get_addresses_by_client(client_name)

    response = {
        'Cod_Fiscal': client_data['Cod_Fiscal'],
        'Aviz_Distributie': client_data['Aviz_Distributie'],
        'Marca': client_data['Marca'],
        'Model': client_data['Model'],
        'Adrese': addresses
    }

    return jsonify(response)

@app.route("/api/clienti")
def search_clients():
    query = request.args.get("q", "")
    clients = get_unique_clients()
    filtered_clients = [
        client for client in clients if query.lower() in client["Nume_Companie"].lower()
    ]
    return jsonify(filtered_clients)

# @app.route("/shutdown", methods=["POST"])
# def shutdown():
#     #Oprește serverul
#      os.kill(os.getpid(), signal.SIGTERM)
#      return "Server stopped."

def open_browser():
    webbrowser.open("http://127.0.0.1:5000/")

if __name__ == "__main__":
    Timer(1, open_browser).start()
    app.run(debug=False)
