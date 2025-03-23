import csv
import random as rnd
from math import radians, sin, cos, sqrt, atan2
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

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
                "neighbors": row["neighbors"].split(", ")  # Split neighbors into a list
            }
            for row in reader
        }
     
    return countries

def random_country(countries):
 
    return rnd.choice(list(countries.keys()))

def get_best_match(user_input, country_names):

    best_match = process.extractOne(user_input, country_names, scorer=fuzz.partial_ratio)
    return best_match

def game():
    countries_data = load_countries()
    country_names = list(countries_data.keys()) 
    target_country = random_country(countries_data)
    target_lat, target_lon = countries_data[target_country]["coordinates"]
    neighbors = countries_data[target_country]["neighbors"]

    print(", ".join(neighbors))

    print("Tahmin etmeye başla!")
    guesses = []  

    while True:
        guess = input("Bir ülke adı girin: ")
        guess = ' '.join([word[0].upper() + word[1:].lower() for word in guess.split()])
        best_match = get_best_match(guess, country_names)
        
        if best_match[1] > 90 and guess != best_match[0]:
            guess2 = best_match[0]
            guess = guess2

        guesses.append(guess)

        if guess.lower() == "quit":
            print(f"Oyun bitti. Doğru cevap: {target_country}")
            break
        
        if guess not in countries_data:
            print("Geçersiz ülke adı, tekrar deneyin.")
            continue 

        guess_lat, guess_lon = countries_data[guess]["coordinates"]
        distance = haversine(guess_lat, guess_lon, target_lat, target_lon)

        if guess in guesses[:-1]:
            print(f"Bu ülkeyi zaten tahmin ettiniz. Mesafe: {distance:.2f} km.")
            continue
        
        if guess in neighbors:
            print(f"Bu ülke komşu bir ülke. {distance:.2f} km.")
            continue
        else:
            print(f"{guess}, mesafe: {distance:.2f} km.")

        if distance == 0:
            print("Tebrikler! Doğru tahmin ettiniz! 🎉")
            a =input("Tekrar oynamak ister misiniz? (E/H): ")
            if a.lower() == "e":
                game()
            else:
                break
    
    return


if __name__ == "__main__":
    game()
