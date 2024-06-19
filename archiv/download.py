import os
from datetime import datetime

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
file_path = os.path.abspath('content/docs/download.md')

# Sicherstellen, dass das Verzeichnis existiert
os.makedirs(os.path.dirname(file_path), exist_ok=True)

# Debug-Ausgabe des Datei-Pfades
print(f"Schreibe in die Datei: {file_path}")

# Öffne die Datei im Schreibmodus, leere den Inhalt und schreibe den neuen Inhalt hinein
# Falls die Datei nicht existiert, wird sie automatisch erstellt
with open(file_path, 'w') as file:
    file.write(initial_content)

print(f"Inhalt erfolgreich in {file_path} geschrieben.")

# Funktion zum Abrufen der Dateiinformationen
def get_file_info(file_path):
    file_info = os.stat(file_path)
    file_size_mb = round(file_info.st_size / (1024 * 1024), 2)
    last_edit = datetime.fromtimestamp(file_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
    file_name = os.path.basename(file_path)
    file_type = 'Ordner' if os.path.isdir(file_path) else 'Datei'
    relative_path = os.path.relpath(file_path, start='static')
    download_link = f"[Download](static/{relative_path})"
    return file_name, last_edit, file_size_mb, file_type, download_link

# Füge Tabelleninhalt mit Dateiinformationen aus dem Ordner 'static' hinzu
table_rows = []
for root, dirs, files in os.walk('static'):
    for file in files:
        file_path = os.path.join(root, file)
        file_name, last_edit, file_size_mb, file_type, download_link = get_file_info(file_path)
        table_rows.append(f"| {file_name} | {last_edit} | {file_size_mb} | {file_type} | {download_link} |\n")

# Debug-Ausgabe der Tabellenzeilen
print("Tabelleninhalt:")
print(''.join(table_rows))

# Füge zusätzlichen Inhalt und Tabelleninhalt in die Datei download.md ein
try:
    with open(file_path, 'a') as file:
        file.write(additional_content)
        file.writelines(table_rows)
    print(f"Zusätzlicher Inhalt und Dateiinformationen erfolgreich in {file_path} eingefügt.")
except Exception as e:
    print(f"Fehler beim Schreiben in die Datei {file_path}: {e}")
