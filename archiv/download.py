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

# Debug-Ausgabe des zusätzlichen Inhalts
print("Zusätzlicher Inhalt:")
print(additional_content)

# Datei-Pfad zur download.md Datei
file_path = os.path.abspath(os.path.join('archiv', 'content', 'docs', 'download.md'))

# Sicherstellen, dass das Verzeichnis existiert
os.makedirs(os.path.dirname(file_path), exist_ok=True)

# Debug-Ausgabe des Datei-Pfades
print(f"Schreibe in die Datei: {file_path}")

# Funktion zum Abrufen der Dateiinformationen
def get_file_info(file_path):
    file_info = os.stat(file_path)
    file_size_mb = round(file_info.st_size / (1024 * 1024), 2)
    last_edit = datetime.fromtimestamp(file_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
    file_name = os.path.basename(file_path)
    file_type = 'Ordner' if os.path.isdir(file_path) else 'Datei'
    relative_path = os.path.relpath(file_path, start=os.path.join('archiv', 'static')).replace(os.sep, '/')
    download_link = f"[Download]({relative_path})"
    return file_name, last_edit, file_size_mb, file_type, download_link

# Erstelle Tabelleninhalt mit Dateiinformationen aus dem Ordner 'archiv/static'
table_rows = []
static_path = os.path.abspath(os.path.join('archiv', 'static'))

# Debug-Ausgabe des Pfads zum static-Ordner
print(f"Durchlaufe den Ordner: {static_path}")

for root, dirs, files in os.walk(static_path):
    for file in files:
        file_path = os.path.join(root, file)
        file_name, last_edit, file_size_mb, file_type, download_link = get_file_info(file_path)
        table_rows.append(f"| {file_name} | {last_edit} | {file_size_mb} | {file_type} | {download_link} |\n")

# Debug-Ausgabe der Tabellenzeilen
print("Tabelleninhalt:")
print(''.join(table_rows))

# Kombiniere initialen Inhalt, zusätzlichen Inhalt und Tabelleninhalt
final_content = initial_content + additional_content + ''.join(table_rows)

# Debug-Ausgabe des finalen Inhalts
print("Finaler Inhalt:")
print(final_content)

file_path = "archiv/content/docs/download.md"
# Schreibe den kombinierten Inhalt in die Datei download.md
try:
    with open(file_path, 'w') as file:
        file.write(final_content)
    print(f"Inhalt erfolgreich in {file_path} geschrieben.")
except Exception as e:
    print(f"Fehler beim Schreiben in die Datei {file_path}: {e}")
