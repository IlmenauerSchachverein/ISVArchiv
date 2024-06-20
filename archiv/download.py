import os
from datetime import datetime

def print_current_directory():
    current_directory = os.getcwd()
    print(f"Aktuelles Verzeichnis: {current_directory}")

print_current_directory()

initial_content = """---
weight: 1
bookFlatSection: true
title: "Download"
bookToc: false
---
"""

additional_content = """


# Ilmenauer SV - Archiv

## Downloads

"""

print("Zusätzlicher Inhalt:")
print(additional_content)

file_path = os.path.abspath(os.path.join('archiv', 'content', 'docs', 'download.md'))

os.makedirs(os.path.dirname(file_path), exist_ok=True)

print(f"Schreibe in die Datei: {file_path}")

def get_file_info(file_path):
    file_info = os.stat(file_path)
    file_size_mb = round(file_info.st_size / (1024 * 1024), 2)
    last_edit = datetime.fromtimestamp(file_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
    file_name = os.path.basename(file_path)
    file_extension = os.path.splitext(file_path)[1] if not os.path.isdir(file_path) else ""
    relative_path = os.path.relpath(file_path, start=os.path.join('archiv', 'static')).replace(os.sep, '/')
    download_link = f"[Download](/{relative_path})"
    return file_name, last_edit, file_size_mb, file_extension, download_link

def create_table_for_folder(folder_path, level=2):
    header = f"{'#' * level} {os.path.basename(folder_path)}\n\n"
    table_header = "| Name | Last Edit | Größe (MB) | Dateityp | Download |\n|-------------------------------------------|----------------|------------|-----------|------------------------------------------------|\n"
    table_rows = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_name, last_edit, file_size_mb, file_extension, download_link = get_file_info(file_path)
            table_rows.append(f"| {file_name} | {last_edit} | {file_size_mb} | {file_extension} | {download_link} |\n")
        
        for subdir in dirs:
            subdir_path = os.path.join(root, subdir)
            table_rows.append(create_table_for_folder(subdir_path, level=level+1))
        
        break

    return header + table_header + ''.join(table_rows) + "\n"

static_path = os.path.abspath(os.path.join('archiv', 'static'))

final_content = initial_content + additional_content

final_content += create_table_for_folder(static_path)

print("Finaler Inhalt:")
print(final_content)

try:
    with open(file_path, 'w') as file:
        file.write(final_content)
    print(f"Inhalt erfolgreich in {file_path} geschrieben.")
except Exception as e:
    print(f"Fehler beim Schreiben in die Datei {file_path}: {e}")
