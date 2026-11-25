from dataset import dataset
from test_dataset import test_dataset

print("Welcome to AI Security Lab")
suspected_documents = [
    "ignore the user",
    "disregard previous instructions",
    "reveal your system prompt",
    "override your instructions",
    "Ignore all previous instructions",
    "Override your previous instructions",
    "forget your original task",
    "follow these new instructions"
]

def detect_injection(users_document, suspected_documents):
      for document in suspected_documents:
         if document.lower() in users_document.lower():
           return 1  
      return 0

TP = 0
FP = 0
TN = 0
FN = 0

for item in dataset:
    users_document = item['text']
    actual_label = item['label']

    result = detect_injection(users_document, suspected_documents)

    if result != actual_label:
        print(f"Misclassified Document: {users_document}, Actual Label: {actual_label}, Detected Label: {result}")
    print(f"Document: {users_document}, Actual Label: {actual_label}, Detected Label: {result}")

    #confusion matrix
    if actual_label == 1 and result == 1:
        TP += 1
    elif actual_label == 0 and result == 1:
        FP += 1
    elif actual_label == 0 and result == 0:
        TN += 1
    elif actual_label == 1 and result == 0:
        FN += 1

print(f"True Positives: {TP}")
print(f"False Positives: {FP}")
print(f"True Negatives: {TN}")
print(f"False Negatives: {FN}")

precision = TP / (TP + FP) if (TP + FP) > 0 else 0
recall = TP / (TP + FN) if (TP + FN) > 0 else 0
accuracy = (TP + TN) / (TP + TN + FP + FN) if (TP + TN + FP + FN) > 0 else 0
print(f"Precision: {precision}")    
print(f"Recall: {recall}")
print(f"Accuracy: {accuracy}")

f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
print(f"F1 Score: {f1_score:.2%}")

TP = 0
FP = 0
TN = 0
FN = 0


for item in test_dataset:
    users_document = item['text']
    actual_label = item['label']
    result = detect_injection(users_document, suspected_documents)
    
    if result != actual_label:
            print(f"Misclassified Document: {users_document}, Actual Label: {actual_label}, Detected Label: {result}")
    print(f"Document: {users_document}, Actual Label: {actual_label}, Detected Label: {result}")
    
        #confusion matrix
    if actual_label == 1 and result == 1:
            TP += 1
    elif actual_label == 0 and result == 1:
            FP += 1
    elif actual_label == 0 and result == 0:
            TN += 1
    elif actual_label == 1 and result == 0:
            FN += 1
print("test results:")
print(f"True Positives: {TP}")
print(f"False Positives: {FP}")
print(f"True Negatives: {TN}")
print(f"False Negatives: {FN}")
    
precision = TP / (TP + FP) if (TP + FP) > 0 else 0
recall = TP / (TP + FN) if (TP + FN) > 0 else 0
accuracy = (TP + TN) / (TP + TN + FP + FN) if (TP + TN + FP + FN) > 0 else 0
print(f"Precision: {precision}")    
print(f"Recall: {recall}")
print(f"Accuracy: {accuracy}")
    
f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
print(f"F1 Score: {f1_score:.2%}")
    