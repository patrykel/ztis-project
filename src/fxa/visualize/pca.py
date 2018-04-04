from fxa.utils import note_to_vec
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns  # noqa


def _prepare_plots():
    sns.set_style("whitegrid")
    sns.set(font_scale=1.5)
    plt.figure()


def _save_plot(filename, extension='pdf'):
    plt.savefig(filename + "." + extension, bbox_inches='tight')


def __get_pca_model(notes):
    pca = PCA(n_components=2)
    notes_vectors = [note_to_vec(note) for note in notes]
    pca.fit(notes_vectors)
    return pca


def visualize_pca_by_lang(notes):
    _prepare_plots()
    pca = __get_pca_model(notes)

    langs = [note.get_lang() for note in notes]
    langs = sorted(set(langs))
    for lang in langs:
        lang_notes = [note for note in notes if note.get_lang() == lang]
        lang_notes_vectors = [note_to_vec(note) for note in lang_notes]
        pca_lang_notes = pca.transform(lang_notes_vectors)
        plt.scatter(pca_lang_notes[:, 0], pca_lang_notes[:, 1], alpha=0.7, label=lang)
    plt.legend()
    _save_plot('lang')


def visualize_pca_by_currency(notes):
    _prepare_plots()
    pca = __get_pca_model(notes)

    currencies = [note.currency for note in notes]
    currencies = sorted(set(currencies))

    colors = iter(sns.color_palette("hls", len(currencies)).as_hex())

    for currency in currencies:
        currency_notes = [note for note in notes if note.currency == currency]
        currency_notes_vectors = [note_to_vec(note) for note in currency_notes]
        pca_currency_notes = pca.transform(currency_notes_vectors)
        plt.scatter(pca_currency_notes[:, 0],
                    pca_currency_notes[:, 1], label=currency, alpha=0.7, color=next(colors))
    plt.legend()
    _save_plot('currency')


def visualize_pca_by_growth(notes):
    _prepare_plots()
    pca = __get_pca_model(notes)

    growths = [note.growth for note in notes]
    growths = sorted(set(growths))

    colors = iter(['#e74c3c', '#2ecc71'])

    for growth in growths:
        growth_notes = [note for note in notes if note.growth == growth]
        growth_notes_vectors = [note_to_vec(note) for note in growth_notes]
        pca_growth_notes = pca.transform(growth_notes_vectors)
        plt.scatter(pca_growth_notes[:, 0],
                    pca_growth_notes[:, 1], label=growth, alpha=0.7, color=next(colors))
    plt.legend()
    _save_plot('growth')
