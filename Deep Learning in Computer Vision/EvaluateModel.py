import os
import numpy as np
import tensorflow as tf
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

from DatasetPreparation import LoadDatasetWithNormalization

def evaluate_model(model_path, test_dir, result_dir, img_size=(128, 128)):
    model = tf.keras.models.load_model(model_path)

    test_dataset = LoadDatasetWithNormalization(test_dir, target_size=img_size, batch_size=32)

    class_names = list(test_dataset.class_indices.keys())
    print(f"Classes: {class_names}")

    y_true = []
    y_pred = []

    total_batches = len(test_dataset)
    print(f"Processing {total_batches} batches...\n")

    for i, (batch_x, batch_y) in enumerate(test_dataset):
        preds = model.predict(batch_x, verbose=0)
        y_true.extend(np.argmax(batch_y, axis=1))
        y_pred.extend(np.argmax(preds, axis=1))

        if (i + 1) % 5 == 0 or (i + 1) == total_batches:
            print(f"Processed {i + 1}/{total_batches} batches...")

        if (i + 1) >= total_batches:
            break

    y_true = np.array(y_true)
    y_pred = np.array(y_pred)

    print("\nClassification Report:\n")
    print(classification_report(y_true, y_pred, target_names=class_names))

    cm = confusion_matrix(y_true, y_pred)
    print("Confusion Matrix:\n")
    print(cm)

    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', xticklabels=class_names, yticklabels=class_names, cmap='Blues')
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.title('Confusion Matrix')
    plt.tight_layout()
    plt.show()

    log_dir = f"./EvaluationLogs/{result_dir}"
    os.makedirs(log_dir, exist_ok=True)

    report = classification_report(y_true, y_pred, target_names=class_names, digits=4)
    report_path = os.path.join(log_dir, "classification_report.txt")
    with open(report_path, "w") as f:
        f.write("Classification Report\n\n")
        f.write(report)
    print(f"Saved classification report to {report_path}")

    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=class_names, yticklabels=class_names)
    plt.title("Confusion Matrix")
    plt.xlabel("Predicted Label")
    plt.ylabel("True Label")
    plt.tight_layout()
    cm_path = os.path.join(log_dir, "confusion_matrix.png")
    plt.savefig(cm_path)
    plt.close()
    print(f"Saved confusion matrix plot to {cm_path}")

    
if __name__ == "__main__":
    RESULT_DIR = "./Split2"
    MODEL_PATH = f"./TrainingOutputs/{RESULT_DIR}/MODEL2.keras"
    TEST_DIR = f"./{RESULT_DIR}/test"
    IMG_SIZE = (128, 128)

    evaluate_model(MODEL_PATH, TEST_DIR, RESULT_DIR, IMG_SIZE)
