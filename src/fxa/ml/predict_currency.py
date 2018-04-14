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

# My new classifiers

# PROPOSED...
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.neural_network import MLPClassifier

# NEW FROM SCIKIT LEARN...
from sklearn.svm import LinearSVC
# from sklearn.naive_bayes import MultinomialNB # input must be non-negative
from sklearn.linear_model import SGDClassifier

from sklearn.linear_model import LassoCV # Can't handle mix of multiclass and continuous
from sklearn.linear_model import Ridge # Can't handle mix of multiclass and continuous
from sklearn.linear_model import BayesianRidge # Can't handle mix of multiclass and continuous
from sklearn.linear_model import PassiveAggressiveClassifier #

# My time measurement
import time

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
    print("\tGetting note vectors...")
    note_vectors = [note_to_vec(note) for note in notes]
    print("\tSplitting train test...")
    X_train, X_test, y_train, y_test = train_test_split(
        note_vectors, predictions, test_size=0.2)
    print("\tFitting...")
    clf.fit(X_train, y_train)
    print("\tPredicting...")
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
        ('Decision Tree', DecisionTreeClassifier()),

        ('GaussianNB', GaussianNB()),
        ('QuadraticDiscriminantAnalysis', QuadraticDiscriminantAnalysis()),
        ('MLPClassifier', MLPClassifier()),

        ('LinearSVC', LinearSVC()),
        ('SGDClassifier', SGDClassifier()),
        ('PassiveAggressiveClassifier', PassiveAggressiveClassifier()),
    ]
    for classifier in CLASSIFIERS:
        print(classifier[0])

        start = time.time()
        score = test_model(notes, predictions, classifier[1])
        end = time.time()
        print("Elapsed time: {}\n".format(end - start))

        scores[classifier[0]] = score
    pprint(sorted(scores.items(), key=operator.itemgetter(1), reverse=True))
