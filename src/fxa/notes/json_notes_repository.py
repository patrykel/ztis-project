from fxa.notes.notes_repository import NotesRepository
from fxa.notes.note import Note
import json


class JsonNotesRepository(NotesRepository):

    def __init__(self, filename):
        self.filename = filename
        self.notes = None

    def get_notes(self):
        if self.notes is None:
            self.notes = []
            with open(self.filename) as data_file:
                data = json.load(data_file)
                for note_dict in data:
                    note = Note(
                        feed="pl_POL",
                        publish_date=note_dict['date'],
                        title=note_dict['title'],
                        content=note_dict['content'],
                        growth=None,
                        currency=None
                    )
                    self.notes.append(note)
        return self.notes
