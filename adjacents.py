import pandas as pd

# Dosyaları oku
globle_df = pd.read_csv("./globle/globle.csv")  # Ana ülke verisi
borders_df = pd.read_csv("./globle/country_borders.csv")  # Komşu ülkeler verisi

# NaN değerleri boş string ile değiştir
borders_df["country_border_name"] = borders_df["country_border_name"].fillna("")

# Komşu ülkeleri gruplayarak virgülle birleştir
borders_grouped = borders_df.groupby("country_name")["country_border_name"].apply(lambda x: ", ".join(x.dropna().astype(str))).reset_index()

# Ana ülke verisi ile birleştir (country sütunu üzerinden)
merged_df = globle_df.merge(borders_grouped, left_on="country", right_on="country_name", how="left")

# Gereksiz tekrar eden sütunu sil
merged_df.drop(columns=["country_name"], inplace=True)

# Yeni sütunu adlandır
merged_df.rename(columns={"country_border_name": "neighbors"}, inplace=True)

# Sonucu yeni CSV dosyasına kaydet
merged_df.to_csv("globle_with_neighbors.csv", index=False)

print("Yeni dosya kaydedildi: globle_with_neighbors.csv")
