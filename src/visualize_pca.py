from fxa.notes.db_notes_repository import DbNotesRepository
from fxa.visualize.pca import visualize_pca_by_lang, visualize_pca_by_currency, visualize_pca_by_growth
import numpy as np


def main():
    notes_repository = DbNotesRepository()
    notes = notes_repository.get_notes()
    notes = np.random.choice(notes, 1000)
    visualize_pca_by_lang(notes)

    currencies_notes = notes_repository.get_all_notes_with_currency()
    visualize_pca_by_currency(currencies_notes)

    growth_notes = notes_repository.get_all_notes_with_growth()
    visualize_pca_by_growth(growth_notes)

if __name__ == "__main__":
    main()
