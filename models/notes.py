# notes.py
import json
import csv
from datetime import datetime

NOTES_FILE = "notes.json"
class Note:
    def __init__(self, id, title, content, timestamp=None):
        self.id = id
        self.title = title
        self.content = content
        self.timestamp = timestamp or datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    def to_dict(self):
        return {"id": self.id, "title": self.title, "content": self.content, "timestamp": self.timestamp}

    @staticmethod
    def from_dict(data):
        return Note(data['id'], data['title'], data['content'], data['timestamp'])

class NoteManager:
    def __init__(self):
        self.notes = self.load_notes()

    def load_notes(self):
        try:
            with open(NOTES_FILE, 'r') as file:
                return [Note.from_dict(note) for note in json.load(file)]
        except FileNotFoundError:
            return []

    def save_notes(self):
        with open(NOTES_FILE, 'w') as file:
            json.dump([note.to_dict() for note in self.notes], file, indent=4)

    def create_note(self, title, content):
        new_id = max((note.id for note in self.notes), default=0) + 1
        new_note = Note(new_id, title, content)
        self.notes.append(new_note)
        self.save_notes()
        print("Note created successfully.")

    def list_notes(self):
        for note in self.notes:
            print(f"{note.id}. {note.title} (Last Modified: {note.timestamp})")

    def view_note_details(self, note_id):
        note = next((n for n in self.notes if n.id == note_id), None)
        if note:
            print(f"Title: {note.title}\nContent: {note.content}\nLast Modified: {note.timestamp}")
        else:
            print("Заметка не найдена")

    def edit_note(self, note_id, new_title, new_content):
        note = next((n for n in self.notes if n.id == note_id), None)
        if note:
            note.title = new_title
            note.content = new_content
            note.timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            self.save_notes()
            print("Note updated successfully.")
        else:
            print("Заметка не найдена")

    def delete_note(self, note_id):
        self.notes = [note for note in self.notes if note.id != note_id]
        self.save_notes()
        print("Заметка удалена")

    def export_to_csv(self, file_name="notes.csv"):
        with open(file_name, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["id", "title", "content", "timestamp"])
            writer.writeheader()
            for note in self.notes:
                writer.writerow(note.to_dict())
        print(f"Заметка экспортирована в {file_name}")

    def import_from_csv(self, file_name="notes.csv"):
        with open(file_name, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.create_note(row["title"], row["content"])
        print(f"Заметка импортирована в {file_name}")