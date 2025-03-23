import csv


def new_data():
    with open("world_country_and_usa_states_latitude_and_longitude_values.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        # İstenen sütunlar
        secilen_sutunlar = ["country_code", "latitude", "longitude", "country"]

        # Yeni dosyaya yaz
        with open("globle.csv", "w", newline="", encoding="utf-8") as f_out:
            writer = csv.DictWriter(f_out, fieldnames=secilen_sutunlar)
            writer.writeheader()

            for row in reader:
                # Eğer herhangi bir sütun boşsa, o satırı atla
                if all(row[col] for col in secilen_sutunlar):
                    writer.writerow({col: row[col] for col in secilen_sutunlar})

    print("Yeni CSV dosyası oluşturuldu, boş değerler çıkarıldı.")


if __name__ == "__main__":
    new_data()
