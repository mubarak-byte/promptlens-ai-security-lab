from datasets import load_dataset
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from collections import Counter
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC


dataset = load_dataset("neuralchemy/Prompt-Injection-Dataset","core")
#inspect the dataset 
print("Downloaded dataset:", dataset)
print("Training examples:", len(dataset['train']))
print("Validation examples:",len(dataset["validation"]))
print("Testing examples:", len(dataset["test"]))

print("Available columns:", dataset["train"].column_names)

counter = Counter(dataset["train"]["label"])
print(counter)
print(dataset["train"].features["label"])

# print("Category_samples:", Counter(dataset["train"]["category"]))
category_counter= Counter()
for item in dataset["train"]:
    if item["label"] == 0 and item["category"] != "benign":
        category_counter[item["category"]] += 1
        print(item)


print(category_counter)

for item in dataset["train"]:
    if item["label"] == 1 and item["category"] == "benign":
        print(item)

train_text = dataset["train"]["text"]
val_text = dataset["validation"]["text"]
val_set = set(val_text)
train_set = set(train_text)
intersection = val_set & train_set
        
print(len(intersection))

normalized_train = [" ".join(text.lower().split()) for text in train_text]
normalized_val = [" ".join(text.lower().split()) for text in val_text]
normalized_intersection = set(normalized_val) & set(normalized_train)
print(len(normalized_intersection))


train_group_ids = dataset["train"]["group_id"]
val_group_ids = dataset["validation"]["group_id"]
test_group_ids = dataset["test"]["group_id"]
train_group_set = set(train_group_ids)
val_group_set = set(val_group_ids)
test_group_set = set(test_group_ids)
group_intersection = val_group_set & train_group_set
group_test_int= val_group_set & test_group_set
print(len(group_intersection))
print(len(group_test_int))


train_texts =[]
train_labels = []
for item in dataset["train"]:
    train_texts.append(item["text"])
    train_labels.append(item["label"])
print("Train texts:", len(train_texts))
print("Train labels:", len(train_labels))

vectorizer = TfidfVectorizer()
train_vectors = vectorizer.fit_transform(train_texts)
X_train = train_vectors
print("Train vectors shape:", X_train.shape)


model = LogisticRegression()
model.fit(X_train, train_labels)
print("Model training completed!")
print(model.coef_.shape)


val_text = []
val_label =[]
for item in dataset["validation"]:
    val_text.append(item["text"])
    val_label.append(item["label"])

val_vector = vectorizer.transform(val_text)
X_val = val_vector
print(X_val.shape)

val_prediction = model.predict(X_val)
print(val_prediction[:10])
print(val_label[:10])


TP = 0
FP = 0
TN = 0
FN = 0

for actual, predicted in zip(val_label, val_prediction):
    if actual == 1 and predicted == 1:
        TP += 1
    elif actual == 0 and predicted == 1:
        FP += 1
    elif actual == 0 and predicted == 0:
        TN += 1
    elif actual == 1 and predicted == 0:
        FN += 1

print(f"True Positives: {TP}")
print(f"False Positives: {FP}") 
print(f"True Negatives: {TN}")
print(f"False Negatives: {FN}")


precision = TP / (TP + FP) if (TP + FP) > 0 else 0
recall = TP / (TP + FN) if (TP + FN) > 0 else 0
accuracy = (TP + TN) / (TP + TN + FP + FN) if (TP + TN + FP + FN) > 0 else 0
f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
print(f"Precision: {precision:.2%}")    
print(f"Recall: {recall:.2%}")
print(f"Accuracy: {accuracy:.2%}")
print(f"F1 Score: {f1_score:.2%}")

fn_indeces= []
for index, (true,predicted)  in enumerate(zip (val_label, val_prediction)):
    if true == 1 and predicted == 0:
        print(index)
        fn_indeces.append(index)

for i in fn_indeces:
     print(i)
     print(dataset["validation"][i]["text"])
     print(dataset["validation"][i]["category"])

from collections import Counter

categories = []

for item in dataset["validation"]:
    if item["category"] == "jailbreak" and item["label"] == 1:
        categories.append(item["category"])

print(Counter(categories))


false_positive_indices=[]
for index, (true,pred) in enumerate(zip(val_label,val_prediction)):
    if true== 0 and pred == 1:
            false_positive_indices.append(index)

print("False postive :",len(false_positive_indices))


fp_categories=[]
for i in false_positive_indices:
    print(dataset["validation"][i]["category"])
    print(len(fp_categories))


benign_category_labels = []

for item in dataset["validation"]:
    if item["category"] == "benign" and item["label"] == 0 or item["category"] =="edge_case" and item["label"] ==0:
     benign_category_labels.append(item["category"])

print(Counter(benign_category_labels))

nb_model = MultinomialNB(alpha=1.0)
nb_model.fit(X_train, train_labels)

print("Training completed ")

nb_predictions = nb_model.predict(X_val)
print(nb_predictions[:10])
print(val_label[:10])

TP = 0
FP = 0
TN = 0
FN = 0

for actual, predicted in zip(val_label, nb_predictions):
    if actual == 1 and predicted == 1:
        TP += 1
    elif actual == 0 and predicted == 1:
        FP += 1
    elif actual == 0 and predicted == 0:
        TN += 1
    elif actual == 1 and predicted == 0:
        FN += 1

print(f"True Positives: {TP}")
print(f"False Positives: {FP}") 
print(f"True Negatives: {TN}")
print(f"False Negatives: {FN}")


precision = TP / (TP + FP) if (TP + FP) > 0 else 0
recall = TP / (TP + FN) if (TP + FN) > 0 else 0
accuracy = (TP + TN) / (TP + TN + FP + FN) if (TP + TN + FP + FN) > 0 else 0
f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
print(f"Precision: {precision:.2%}")    
print(f"Recall: {recall:.2%}")
print(f"Accuracy: {accuracy:.2%}")
print(f"F1 Score: {f1_score:.2%}")


svm_model = LinearSVC(C=1.0,random_state=42)
svm_model.fit(X_train,train_labels)
print("Training complete")
print(svm_model.coef_.shape)

svm_predictions= svm_model.predict(X_val)
print(svm_predictions[:10])
print(val_label[:10])

TP = 0
FP = 0
TN = 0
FN = 0

for actual, predicted in zip(val_label, svm_predictions):
    if actual == 1 and predicted == 1:
        TP += 1
    elif actual == 0 and predicted == 1:
        FP += 1
    elif actual == 0 and predicted == 0:
        TN += 1
    elif actual == 1 and predicted == 0:
        FN += 1

print(f"True Positives: {TP}")
print(f"False Positives: {FP}") 
print(f"True Negatives: {TN}")
print(f"False Negatives: {FN}")


precision = TP / (TP + FP) if (TP + FP) > 0 else 0
recall = TP / (TP + FN) if (TP + FN) > 0 else 0
accuracy = (TP + TN) / (TP + TN + FP + FN) if (TP + TN + FP + FN) > 0 else 0
f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
print(f"Precision: {precision:.2%}")    
print(f"Recall: {recall:.2%}")
print(f"Accuracy: {accuracy:.2%}")
print(f"F1 Score: {f1_score:.2%}")


svm_fp_indices=[]
for index, (true,pred) in enumerate(zip(val_label,svm_predictions)):
    if true== 0 and pred == 1:
            svm_fp_indices.append(index)

print("False postive :",len(svm_fp_indices))


for i in svm_fp_indices:
     print(dataset["validation"][i]["category"])

from collections import Counter

svm_fn_indices = []

for index, (true, pred) in enumerate(zip(val_label, svm_predictions)):
    if true == 1 and pred == 0:
        svm_fn_indices.append(index)

print("False Negatives:", len(svm_fn_indices))
print("False Negative Indices:", svm_fn_indices)

# Count false-negative categories
svm_fn_categories = Counter()

for index in svm_fn_indices:
    category = dataset["validation"][index]["category"]
    svm_fn_categories[category] += 1

print("False Negative Categories:", svm_fn_categories)

# Logistic Regression false-negative indices
lr_fn_indices = [24, 29, 32, 60, 72, 73, 708, 858]

# Convert both lists to sets
lr_fn_set = set(lr_fn_indices)
svm_fn_set = set(svm_fn_indices)

# 1. Documents both models missed
both_missed = lr_fn_set & svm_fn_set

# 2. Documents only Logistic Regression missed
lr_only = lr_fn_set - svm_fn_set

# 3. Documents only LinearSVC missed
svm_only = svm_fn_set - lr_fn_set

print("Both models missed:", sorted(both_missed))
print("Only Logistic Regression missed:", sorted(lr_only))
print("Only LinearSVC missed:", sorted(svm_only))

print("\nTotal missed by both:", len(both_missed))
print("Total missed only by LR:", len(lr_only))
print("Total missed only by SVM:", len(svm_only))


# One example from each failure group
sample_indices = [24, 72, 16]

for index in sample_indices:
    sample = dataset["validation"][index]

    print("\n" + "=" * 60)
    print("Index:", index)
    print("Category:", sample["category"])
    print("Actual Label:", sample["label"])
    print("Logistic Regression:", val_prediction[index])
    print("LinearSVC:", svm_predictions[index])
    print("Text:", sample["text"])

    sample_indices = [24, 72, 16]

lr_scores = model.decision_function(X_val[sample_indices])
svm_scores = svm_model.decision_function(X_val[sample_indices])

for index, lr_score, svm_score in zip(
    sample_indices, lr_scores, svm_scores
):
    print(f"\nDocument: {index}")
    print(f"Logistic Regression score: {lr_score:.4f}")
    print(f"LinearSVC score: {svm_score:.4f}")



# Challenge 37 — Step 2
# Inspect TF-IDF features for document 16

index = 16

# Get the TF-IDF feature names
feature_names = vectorizer.get_feature_names_out()

# Get document 16 from the validation feature matrix
document_vector = X_val[index]

# Find the indices of features present in the document
active_indices = document_vector.nonzero()[1]

print("Document Index:", index)
print("Category:", dataset["validation"][index]["category"])
print("Actual Label:", val_label[index])

print("\nTF-IDF Features:")
print("-" * 50)

for feature_index in active_indices:
    feature_name = feature_names[feature_index]
    tfidf_value = document_vector[0, feature_index]

    print(f"{feature_name:<25} {tfidf_value:.4f}")

print("-" * 50)
print("Total Active Features:", len(active_indices))

import numpy as np

index = 16

feature_names = vectorizer.get_feature_names_out()
document_vector = X_val[index]
active_indices = document_vector.nonzero()[1]

models = {
    "Logistic Regression": model,
    "LinearSVC": svm_model
}

for model_name, classifier in models.items():

    print("\n" + "=" * 60)
    print(model_name)

    contributions = []

    for feature_index in active_indices:
        feature = feature_names[feature_index]
        tfidf = float(document_vector[0, feature_index])
        weight = classifier.coef_[0, feature_index]

        contribution = tfidf * weight

        contributions.append((feature, contribution))

    # Sort from most positive to most negative
    contributions.sort(key=lambda x: x[1], reverse=True)

    print("\nTOP 5 MALICIOUS-SUPPORTING FEATURES")
    for feature, value in contributions[:5]:
        print(f"{feature:<20} {value:+.4f}")

    print("\nTOP 5 BENIGN-SUPPORTING FEATURES")
    for feature, value in contributions[-5:]:
        print(f"{feature:<20} {value:+.4f}")

    # Reconstruct the model's decision score
    total_contribution = sum(value for _, value in contributions)
    decision_score = total_contribution + classifier.intercept_[0]

    print("\nReconstructed decision score:", round(decision_score, 4))
    print("Model decision score:",
          round(classifier.decision_function(document_vector)[0], 4))

    
from sklearn.metrics import confusion_matrix, classification_report

test_texts = dataset["test"]["text"]
test_labels = dataset["test"]["label"]

X_test = vectorizer.transform(test_texts)
test_predictions = svm_model.predict(X_test)

print("Test examples:", len(test_labels))
print("Confusion Matrix:")
print(confusion_matrix(test_labels, test_predictions, labels=[0, 1]))

print("\nClassification Report:")
print(classification_report(
    test_labels,
    test_predictions,
    labels=[0, 1],
    target_names=["Benign", "Malicious"],
    digits=4
))


import joblib
from sklearn.pipeline import Pipeline

promptlens_pipeline = Pipeline([
    ("tfidf", vectorizer),
    ("classifier", svm_model)
])

joblib.dump(promptlens_pipeline, "promptlens_model.joblib")

print("PromptLens model saved successfully!")
