from flask import Flask, render_template, jsonify
import random

app = Flask(__name__)

# Data jumlah ASN yang naik pangkat
data = {
    "2021": 1802,
    "2022": 1584,
    "2023": 2039
}

# Fungsi Monte Carlo untuk prediksi jumlah ASN naik pangkat
def monte_carlo_simulation(data):
    tahun = list(data.keys())
    jumlah = list(data.values())
    total = sum(jumlah)
    
    # Hitung probabilitas
    probabilitas = [j / total for j in jumlah]
    
    # Generate bilangan acak dan tentukan prediksi
    predictions = []
    for _ in range(5):  # Generate 5 prediksi
        rand = random.random()
        cumulative_prob = 0
        for i, prob in enumerate(probabilitas):
            cumulative_prob += prob
            if rand <= cumulative_prob:
                predictions.append(jumlah[i])
                break
    return predictions


@app.route('/')
def index():
    predictions = monte_carlo_simulation(data)
    predictions_with_index = list(enumerate(predictions, start=1))
    print(predictions_with_index)  # Debug: cek format data
    return render_template('index.html', data=data, predictions=predictions_with_index)


# Rute untuk mengembalikan prediksi baru (AJAX)
@app.route('/generate_predictions', methods=['GET'])
def generate_predictions():
    predictions = monte_carlo_simulation(data)
    return jsonify(predictions=predictions)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=9898)
