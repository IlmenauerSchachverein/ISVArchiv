import os
import hashlib
from datetime import datetime
import zipfile

def print_current_directory():
    current_directory = os.getcwd()
    print(f"Aktuelles Verzeichnis: {current_directory}")

print_current_directory()

def zip_folder(folder_path, zip_path):
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, start=folder_path)
                zipf.write(file_path, arcname)

def create_zip_archives_for_static():
    static_path = os.path.abspath(os.path.join('archiv', 'static'))
    for root, dirs, _ in os.walk(static_path):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            zip_path = f"{dir_path}.zip"
            zip_folder(dir_path, zip_path)
            print(f"Archiv '{zip_path}' erfolgreich erstellt.")

create_zip_archives_for_static()

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
    sha256_hash = get_sha256(file_path)
    return file_name, last_edit, file_size_mb, file_extension, download_link, sha256_hash

def get_sha256(file_path):
    sha256 = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
    except Exception as e:
        print(f"Fehler beim Berechnen des SHA256-Hashwerts für {file_path}: {e}")
        return ""
    return sha256.hexdigest()

def create_table_for_folder(folder_path, level=2):
    header = f"{'#' * level} {os.path.basename(folder_path)}\n\n"
    table_header = "| Name | Last Edit | Größe (MB) | Dateityp | Download | SHA256 |\n|-------------------------------------------|----------------|------------|-----------|------------------------------------------------|------------------------------------------------|\n"
    table_rows = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_name, last_edit, file_size_mb, file_extension, download_link, sha256_hash = get_file_info(file_path)
            table_rows.append(f"| {file_name} | {last_edit} | {file_size_mb} | {file_extension} | {download_link} | {sha256_hash} |\n")
        
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

# Erstellen der Datei _init.md im Ordner archiv/docs/content/Downloads
init_file_path = os.path.abspath(os.path.join('archiv', 'docs', 'content', 'Downloads', '_init.md'))
init_content = """# Downloads
"""

try:
    os.makedirs(os.path.dirname(init_file_path), exist_ok=True)
    with open(init_file_path, 'w') as file:
        file.write(init_content)
    print(f"Datei erfolgreich erstellt: {init_file_path}")
except Exception as e:
    print(f"Fehler beim Erstellen der Datei {init_file_path}: {e}")
