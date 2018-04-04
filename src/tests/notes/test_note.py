import unittest
from fxa.notes.note import Note


class TestNote(unittest.TestCase):

    def test_get_lang(self):
        note = Note()
        note.feed = "fr_FRA_lmonde_int"
        self.assertEqual(note.get_lang(), "fr")
