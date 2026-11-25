from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
documents =[
    "Ignore user instructions",
    "Follow user instructions",
    "Ignore previous instructions",
]

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(documents)
print(X.toarray())
print(vectorizer.get_feature_names_out())
print(X.toarray().shape)

tfidf_documents=[
    "override system instructions",
    "override system configuration",
    "the system is secure",
    "the system is working",
    "the system is available",
]

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(tfidf_documents)
print(X.toarray())
print(vectorizer.get_feature_names_out())