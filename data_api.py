import kagglehub
import shutil
import os

# Veri kümesini indir
path = kagglehub.dataset_download("paultimothymooney/latitude-and-longitude-for-every-country-and-state")

# Çalışma dizini
target_dir = os.getcwd()  # Çalıştığın dizin

# İndirilen dizindeki dosyaları hedef dizine taşı
for file_name in os.listdir(path):
    full_file_name = os.path.join(path, file_name)
    if os.path.isfile(full_file_name):
        shutil.move(full_file_name, target_dir)

print("Dosyalar başarıyla çalışma dizinine taşındı:", target_dir)
