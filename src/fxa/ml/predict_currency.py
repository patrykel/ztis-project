from fxa.utils import note_to_vec
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import datetime
from pprint import pprint
import operator
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import BernoulliNB
from sklearn.tree import DecisionTreeClassifier


PREDICTION_WINDOW = 7  # in days

CHANGE_THRESHOLD = 0.001


def get_predictions(note, currency_repository):
    note_date = note.publish_date
    prediction_date = note_date + datetime.timedelta(days=PREDICTION_WINDOW)
    currency_value = currency_repository.get_currency_rate(
        "EUR", "USD", note_date.date())
    future_currency_value = currency_repository.get_currency_rate(
        "EUR", "USD", prediction_date.date()
    )
    return currency_value, future_currency_value


def generate_trend_prediction(note, currency_repository):
    currency_value, future_currency_value = get_predictions(
        note, currency_repository)
    diff = abs(future_currency_value.value -
               currency_value.value) / currency_value.value
    if diff < CHANGE_THRESHOLD:
        return 0
    if future_currency_value.value > currency_value.value:
        return 1
    else:
        return -1


def __note_has_currency_rate(note, currency_repository):
    currency_value, future_currency_value = get_predictions(
        note, currency_repository)
    return currency_value is not None and future_currency_value is not None


def test_model(notes, predictions, clf):
    note_vectors = [note_to_vec(note) for note in notes]
    X_train, X_test, y_train, y_test = train_test_split(
        note_vectors, predictions, test_size=0.2)
    clf.fit(X_train, y_train)
    generated_predictions = clf.predict(X_test)
    return accuracy_score(y_test, generated_predictions)


def run_ml_tests(notes, currency_repository):
    scores = {}
    notes = list(filter(lambda note: __note_has_currency_rate(
        note, currency_repository), notes))
    predictions = [generate_trend_prediction(note, currency_repository)
                   for note in notes]

    prediction_types = set(predictions)
    for p_type in prediction_types:
        print(p_type, predictions.count(p_type))

    print("Testing classifiers")

    CLASSIFIERS = [
        ('RandomForest', RandomForestClassifier()),
        ('LogisticRegression', LogisticRegression()),
        ('KNN', KNeighborsClassifier()),
        ('SVM rbf', SVC()),
        ('AdaBoost', AdaBoostClassifier()),
        ('Bernoulli NB', BernoulliNB()),
        ('Decision Tree', DecisionTreeClassifier())
    ]
    for classifier in CLASSIFIERS:
        print(classifier[0])
        score = test_model(notes, predictions, classifier[1])
        scores[classifier[0]] = score
    pprint(sorted(scores.items(), key=operator.itemgetter(1), reverse=True))
