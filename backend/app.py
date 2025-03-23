import csv
import random
from math import radians, sin, cos, sqrt, atan2
from flask import Flask, request, jsonify
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # CORS'yi aktif hale getiriyoruz

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Dünya'nın yarıçapı (km)
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c

def load_countries():
    with open("globle.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return {row["country"]: (float(row["latitude"]), float(row["longitude"])) for row in reader}

def get_best_match(user_input, country_names):
    best_match = process.extractOne(user_input, country_names, scorer=fuzz.partial_ratio)
    return best_match

@app.route('/calculate_distance', methods=['POST'])
def calculate_distance():
    data = request.get_json()
    guess = data.get('guess', '').strip()

    if not guess:
        return jsonify({'error': 'Lütfen bir ülke adı girin.'}), 400

    countries_data = load_countries()
    country_names = list(countries_data.keys())
    target_country = random.choice(list(countries_data.keys()))  # Rastgele bir ülke seç
    target_lat, target_lon = countries_data[target_country]

    best_match = get_best_match(guess, country_names)
    best_match_country = best_match[0]

    if best_match[1] > 90 and guess != best_match_country:
        guess = best_match_country

    if guess not in countries_data:
        return jsonify({'error': 'Geçersiz ülke adı, tekrar deneyin.'}), 400

    guess_lat, guess_lon = countries_data[guess]
    distance = haversine(guess_lat, guess_lon, target_lat, target_lon)

    lat_direction = "Kuzey" if guess_lat > target_lat else "Güney"
    lon_direction = "Doğu" if guess_lon > target_lon else "Batı"

    # Doğru tahmin yapıldı mı kontrolü
    if distance == 0:
        return jsonify({
            'message': 'Tebrikler! Doğru tahmin ettiniz!',
            'best_match': best_match_country,
            'distance': distance,
            'lat_direction': lat_direction,
            'lon_direction': lon_direction
        })

    return jsonify({
        'best_match': best_match_country,
        'distance': distance,
        'lat_direction': lat_direction,
        'lon_direction': lon_direction
    })

@app.route('/random_country', methods=['GET'])
def get_random_country():
    country = random.choice(list(load_countries().keys()))  # Rastgele bir ülke seç
    return jsonify({"country": country})

@app.route('/reset_game', methods=['GET'])
def reset_game():
    """Yeni bir oyun başlatır, yani rastgele ülke seçer."""
    country = random.choice(list(load_countries().keys()))  # Yeni rastgele ülke seç
    return jsonify({"country": country})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
