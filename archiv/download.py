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

# Funktion zum Erstellen einer Tabelle für einen Ordner
def create_table_for_folder(folder_path, level=2):
    header = f"{'#' * level} {os.path.basename(folder_path)}\n\n"
    table_header = "| Name | Last Edit | Größe (MB) | Datei Typ | Download |\n|-------------------------------------------|----------------|------------|-----------|------------------------------------------------|\n"
    table_rows = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_name, last_edit, file_size_mb, file_type, download_link = get_file_info(file_path)
            table_rows.append(f"| {file_name} | {last_edit} | {file_size_mb} | {file_type} | {download_link} |\n")
        
        # Durchlaufe auch alle Unterverzeichnisse
        for subdir in dirs:
            subdir_path = os.path.join(root, subdir)
            table_rows.append(create_table_for_folder(subdir_path, level=level+1))
        
        break

    return header + table_header + ''.join(table_rows) + "\n"

# Hauptverzeichnis 'static'
static_path = os.path.abspath(os.path.join('archiv', 'static'))

# Initialer finaler Inhalt
final_content = initial_content + additional_content

# Erstelle Tabellen für das Hauptverzeichnis 'static' und alle Unterverzeichnisse
final_content += create_table_for_folder(static_path)

# Debug-Ausgabe des finalen Inhalts
print("Finaler Inhalt:")
print(final_content)

# Schreibe den kombinierten Inhalt in die Datei download.md
try:
    with open(file_path, 'w') as file:
        file.write(final_content)
    print(f"Inhalt erfolgreich in {file_path} geschrieben.")
except Exception as e:
    print(f"Fehler beim Schreiben in die Datei {file_path}: {e}")
