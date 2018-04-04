from abc import ABCMeta, abstractmethod


class NotesRepository(metaclass=ABCMeta):

    @abstractmethod
    def get_notes(self):
        pass
