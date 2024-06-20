file_path = 'archiv/content/docs/Downloads/_init.md'

content = """# Downloads
"""

try:
    with open(file_path, 'w') as file:
        file.write(content)
    print(f"Datei erfolgreich erstellt: {file_path}")
except Exception as e:
    print(f"Fehler beim Erstellen der Datei {file_path}: {e}")
