import os
import zipfile
from datetime import datetime
import shutil

# Funktion, um das aktuelle Verzeichnis zu überprüfen
def print_current_directory():
    current_directory = os.getcwd()
    print(f"Aktuelles Verzeichnis: {current_directory}")

print_current_directory()

# Inhalt, der initial in die Datei download.md geschrieben werden soll
initial_content = """---
weight: 1
bookFlatSection: true
title: "Download"
bookToc: false
---
"""

# Zusätzlicher Inhalt, der in die Datei download.md geschrieben werden soll
additional_content = """


# Ilmenauer SV - Archiv

## Downloads

# Gerd Fornahl Turnier 2024

## Downloads

| Name                                      | Last Edit      | Größe (MB) | Datei Typ | Download                                       |
|-------------------------------------------|----------------|------------|-----------|------------------------------------------------|
"""

# Datei-Pfad zur download.md Datei
file_path = os.path.abspath('archiv/content/docs/download.md')

# Sicherstellen, dass das Verzeichnis existiert
os.makedirs(os.path.dirname(file_path), exist_ok=True)

# Debug-Ausgabe des Datei-Pfades
print(f"Schreibe in die Datei: {file_path}")

# Öffne die Datei im Schreibmodus, leere den Inhalt und schreibe den neuen Inhalt hinein
# Falls die Datei nicht existiert, wird sie automatisch erstellt
with open(file_path, 'w') as file:
    file.write(initial_content)

print(f"Inhalt erfolgreich in {file_path} geschrieben.")

# Funktion zum Erstellen eines ZIP-Archivs aus einem Ordner
def zip_folder(folder_name, zip_name):
    zip_path = os.path.abspath(os.path.join('archiv/static', zip_name))
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_name):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, start=folder_name)
                zipf.write(file_path, arcname)
    print(f"Ordner '{folder_name}' erfolgreich in '{zip_path}' umgewandelt.")
    shutil.move(zip_path, os.path.join('archiv/static', zip_name))
    print(f"Archiv '{zip_name}' erfolgreich in den Ordner 'archiv/static' verschoben.")

# Ordner, die in ZIP-Archive umgewandelt werden sollen
folders_to_zip = ['archiv/public', 'archiv/static']
zip_filenames = ['ISVArchiv_public.zip', 'ISVArchiv_static.zip']

# Erstelle ZIP-Archive für die angegebenen Ordner und verschiebe sie in den Ordner 'archiv/static'
for folder, zip_name in zip(folders_to_zip, zip_filenames):
    zip_folder(folder, zip_name)

# Funktion zum Abrufen der Dateiinformationen
def get_file_info(file_path):
    file_info = os.stat(file_path)
    file_size_mb = round(file_info.st_size / (1024 * 1024), 2)
    last_edit = datetime.fromtimestamp(file_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
    file_name = os.path.basename(file_path)
    file_type = 'Ordner' if os.path.isdir(file_path) else 'Datei'
    relative_path = os.path.relpath(file_path, start='archiv/static')
    download_link = f"[Download](static/{relative_path})"
    return file_name, last_edit, file_size_mb, file_type, download_link

# Füge Tabelleninhalt mit Dateiinformationen aus dem Ordner 'archiv/static' hinzu
table_rows = []
for root, dirs, files in os.walk('archiv/static'):
    for file in files:
        file_path = os.path.join(root, file)
        file_name, last_edit, file_size_mb, file_type, download_link = get_file_info(file_path)
        table_rows.append(f"| {file_name} | {last_edit} | {file_size_mb} | {file_type} | {download_link} |\n")

# Debug-Ausgabe der Tabellenzeilen
print("Tabelleninhalt:")
print(''.join(table_rows))

# Füge zusätzlichen Inhalt und Tabelleninhalt in die Datei download.md ein
with open(file_path, 'a') as file:
    file.write(additional_content)
    file.writelines(table_rows)

print(f"Zusätzlicher Inhalt und Dateiinformationen erfolgreich in {file_path} eingefügt.")
