file_path = '/home/runner/work/ISVArchiv/ISVArchiv/archiv/content/docs/Download/_init.md'

content = """# Downloads
"""

try:
    with open(file_path, 'w') as file:
        file.write(content)
    print(f"Datei erfolgreich erstellt: {file_path}")
except Exception as e:
    print(f"Fehler beim Erstellen der Datei {file_path}: {e}")
