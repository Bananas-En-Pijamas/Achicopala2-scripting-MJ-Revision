import os
import requests
from bs4 import BeautifulSoup
import shutil

# Crear carpetas si no existen cambio del if por un for más os.makedirs para crear las carpetas
for folder in ["libros", "temporal"]:
    os.makedirs(folder, exist_ok=True)#exist_ok=True para evitar la necesidad de verificar si la carpeta ya existe antes de crearla

# URL base
base_url = "https://www.conaliteg.sep.gob.mx/"

# URL de la página principal
main_url = "https://www.conaliteg.sep.gob.mx/primaria.html"

# Realizar solicitud HTTP a la página principal
response = requests.get(main_url)
soup = BeautifulSoup(response.content, "html.parser")

# Encontrar y almacenar enlaces
links = soup.find_all("a", href=True)
valid_links = []

for link in links:#bucle for anidado para iterar tanto en las valid_links como en el rango de números de imagen
    if "2023/" in link["href"] and link["href"].endswith(".htm"):
        file_name = link["href"].split("/")[-1]
        folder_name = file_name.split(".")[0][-5:]
        valid_links.append(folder_name)

# URL base de las imágenes
image_base_url = "https://www.conaliteg.sep.gob.mx/2023/c/{}/{}.jpg"

# Descargar y guardar las imágenes en la carpeta "temporal",  f-strings para formatear las cadenas de nombres de archivo e imágenes.
for folder_name in valid_links:
    for image_number in range(401):
        image_download_url = image_base_url.format(folder_name, str(image_number).zfill(3))
        image_path = os.path.join("temporal", f"{folder_name}_{image_number:03d}.jpg")
        if not os.path.exists(image_path):
            image_response = requests.get(image_download_url)
            if image_response.status_code == 200:
                with open(image_path, "wb") as f:
                    f.write(image_response.content)

print("Descargas completadas")

# Mover archivos de la carpeta temporal a las subcarpetas correspondientes en "libros"
temporal_folder = "temporal"
libros_folder = "libros"

for file_name in os.listdir(temporal_folder):
    if file_name.endswith(".jpg"):
        folder_name = file_name.split("_")[0]
        temp_file_path = os.path.join(temporal_folder, file_name)
        subfolder_path = os.path.join(libros_folder, folder_name)
        os.makedirs(subfolder_path, exist_ok=True)
        new_file_path = os.path.join(subfolder_path, file_name)
        shutil.move(temp_file_path, new_file_path)

print("Movimiento de archivos completado.")