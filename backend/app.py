from flask import Flask, request, jsonify, session
import csv
import random as rnd
from math import radians, sin, cos, sqrt, atan2
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
app.secret_key = "supersecretkey"  # Session için gerekli

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Dünya'nın yarıçapı (km)
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

def load_countries():
    with open("./globle/datas/globle_with_neighbors.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        countries = {
            row["country"]: {
                "coordinates": (float(row["latitude"]), float(row["longitude"])),
                "neighbors": row["neighbors"].split(", ")
            }
            for row in reader
        }
    return countries

countries_data = load_countries()
country_names = list(countries_data.keys())

def get_best_match(user_input, country_names):
    best_match = process.extractOne(user_input, country_names, scorer=fuzz.partial_ratio)
    return best_match

@app.route("/random-country", methods=["GET"])
def random_country():
    country = rnd.choice(country_names)
    return jsonify({"random_country": country})

@app.route("/neighbors/<country>", methods=["GET"])
def get_neighbors(country):
    country = country.title()
    if country in countries_data:
        return jsonify({"country": country, "neighbors": countries_data[country]["neighbors"]})
    return jsonify({"error": "Geçersiz ülke adı."}), 400

@app.route("/distance", methods=["POST"])
def calculate_distance():
    data = request.get_json()
    country1 = data.get("country1", "").title()
    country2 = data.get("country2", "").title()
    
    if country1 not in countries_data or country2 not in countries_data:
        return jsonify({"error": "Geçersiz ülke adı."}), 400
    
    lat1, lon1 = countries_data[country1]["coordinates"]
    lat2, lon2 = countries_data[country2]["coordinates"]
    distance = haversine(lat1, lon1, lat2, lon2)
    
    return jsonify({"country1": country1, "country2": country2, "distance_km": round(distance, 2)})

@app.route("/best-match", methods=["POST"])
def best_match():
    data = request.get_json()
    user_input = data.get("country", "").strip()
    match = get_best_match(user_input, country_names)
    
    if match:
        return jsonify({"input": user_input, "best_match": match[0], "match_score": match[1]})
    return jsonify({"error": "Eşleşme bulunamadı."}), 400

if __name__ == "__main__":
    app.run(debug=True ,port=5001)
