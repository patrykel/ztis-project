from fxa.config.db import db_connect
from fxa.notes.csv_notes_repository import CsvNotesRepository
from fxa.notes.json_notes_repository import JsonNotesRepository
from fxa.notes.note import Base
from sqlalchemy.orm import sessionmaker
import os


def import_notes_directory(directory_name,
                           default_filename='rss_unique.csv'):
    con, meta = db_connect()
    Base.metadata.create_all(con)
    Session = sessionmaker(bind=con)
    session = Session()
    for root, subdirs, files in os.walk(directory_name):
        for file_name in files:
            if file_name == default_filename:
                file_path = os.path.join(root, file_name)
                print("Importing:", file_path)
                file_extension = default_filename.split('.')[-1]
                if file_extension == 'csv':
                    import_notes_single_csv(file_path, session)
                elif file_extension == 'json':
                    import_notes_single_json(file_path, session)


def import_notes_single_csv(csv_filename, session):
    notes_repository = CsvNotesRepository(csv_filename)
    notes = notes_repository.get_notes()
    notes = _filter_notes(notes)
    session.add_all(notes)
    session.commit()


def _filter_notes(notes):
    return list(filter(_is_note_complete, notes))


def _is_note_complete(note):
    return note.feed and \
        note.publish_date and \
        note.title and \
        note.content

def import_notes_single_json(json_filename, session):
    notes_respository = JsonNotesRepository(json_filename)
    notes = notes_respository.get_notes()
    session.add_all(notes)
    session.commit()
