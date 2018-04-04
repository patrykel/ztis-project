from fxa.notes.notes_repository import NotesRepository
from fxa.config.db import get_session
from fxa.notes.note import Note
from sqlalchemy import or_


class DbNotesRepository(NotesRepository):

    def get_notes(self):
        session = get_session()
        return session.query(Note).all()

    def get_notes_by_language(self, lang):
        session = get_session()

        return session.query(Note)\
            .filter(Note.feed.like("{}_%".format(lang)))\
            .all()

    def get_note_by_id(self, id):
        session = get_session()
        return session.query(Note) \
            .get(int(id))

    def get_notes_by_language_with_session(self, lang):
        session = get_session()

        return session, session.query(Note)\
            .filter(Note.feed.like("{}_%".format(lang)))\
            .all()

    def get_all_notes_with_currency(self):
        session = get_session()
        return session.query(Note) \
            .filter(Note.currency != '') \
            .all()

    def get_notes_by_currency(self, curency):
        session = get_session()
        return session.query(Note) \
            .filter(Note.currency == curency) \
            .all()

    def get_all_notes_with_growth(self):
        session = get_session()
        return session.query(Note) \
            .filter(or_(Note.growth == True, Note.growth == False)) \
            .all()
