from fxa.notes.notes_repository import NotesRepository
from fxa.notes.note import Note
import csv


class CsvNotesRepository(NotesRepository):

    def __init__(self, filename):
        self.filename = filename
        self.notes = None

    def get_notes(self):
        if self.notes is None:
            self.notes = []
            with open(self.filename, 'r') as f:
                reader = csv.DictReader(f, delimiter='\t')
                for note_line in reader:
                    note = Note(
                        feed=note_line['feed'],
                        publish_date=note_line['time'],
                        title=note_line['text1'],
                        content=note_line['text2'],
                        growth=None,
                        currency=None
                    )
                    self.notes.append(note)
        return self.notes
