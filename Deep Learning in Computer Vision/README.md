# Deep Learning in Computer Vision

Image classification system using Deep Convolutional Neural Networks for the Intel Image Classification dataset with 6 classes: buildings, forest, glacier, mountain, sea, and street.

## 📋 Overview

This is an adaptation of the **Systems with Machine Learning** project tailored for the Intel image classification task. The course focuses on practical deep learning applications with emphasis on data augmentation, robust model evaluation, and accuracy improvement techniques.

**Dataset**: [Intel Image Classification (Kaggle)](https://www.kaggle.com/datasets/puneet6060/intel-image-classification)

## 🎯 Course Objectives

- Implement deep CNN architectures for multi-class image classification
- Develop comprehensive data preprocessing and augmentation strategies
- Explore multiple methods for improving model accuracy
- Evaluate models across multiple data splits for robust assessment
- Apply best practices in machine learning workflow design

## 🏗️ System Architecture

### Neural Network Model
```
Input (128×128×3)
    ↓
Conv2D(64) → MaxPool
    ↓
Conv2D(128) → MaxPool
    ↓
Conv2D(256) → MaxPool
    ↓
Conv2D(512) → MaxPool
    ↓
Flatten → Dense(512, ReLU) → Dropout(0.5) → Dense(6, Softmax)
```

**Architecture Details:**
- 4 convolutional layers with increasing filters (64→128→256→512)
- Max pooling after each convolution block
- Flatten layer followed by dense layers
- Dropout (0.5) for regularization
- Adam optimizer (learning rate: 1e-4)
- Categorical crossentropy loss

## 🔬 Accuracy Improvement Methods Tested

### 1. **Data Augmentation**
Applied comprehensive augmentation to training data:
- Rotation (±20°)
- Zoom (±15%)
- Width/Height shifts (±10 pixels)
- Horizontal & vertical flips
- Brightness adjustment (0.5-2.0×)

### 2. **Model Checkpointing**
- Saves best models based on validation accuracy
- Prevents overfitting and disk space waste
- Tracks validation performance per epoch

### 3. **Early Stopping**
- Monitors validation accuracy with patience=10
- Automatically stops training when accuracy plateaus
- Restores best weights after training

### 4. **Multi-Split Validation**
Three independent data split strategies:
- **Split 1-3**: Different random train/val/test partitions (64%/16%/20%)
- Ensures model generalization across different data distributions
- Detects potential overfitting issues

### 5. **Hyperparameter Tuning**
Configurable parameters:
- Batch size: 32
- Epochs: 30 (with early stopping)
- Learning rate: 1e-4
- Image size: 128×128 pixels
- Train/val/test ratios: 64%/16%/20%

### 6. **GPU Memory Optimization**
- Memory growth configuration for efficient GPU utilization
- Batch-wise evaluation to prevent memory overflow
- Garbage collection between evaluations

## 🛠️ Core Components

### 1. **DatasetPreparation.py**
```python
CopySplitDataFromDir()           # Split dataset into train/val/test
StandardizeAndAugmentData()      # Apply augmentation and normalization
LoadDatasetWithNormalization()   # Load images with streaming
```

### 2. **ModelTraining.py**
```python
CreateModel()          # Build CNN architecture
TrainAndEvaluate()    # Train with callbacks and monitoring
TrainSplit()          # Train on specific split
FindBestModel()       # Locate best checkpoint
GeneratePlot()        # Visualize training history
```

### 3. **EvaluateModel.py**
```python
evaluate_model()      # Comprehensive model evaluation
                      # - Accuracy, Precision, Recall, F1-Score
                      # - Confusion Matrix
                      # - Classification Reports
```

### 4. **ModelTesting.py**
```python
MultiModelSplit1Evaluator  # Compare multiple trained models
                           # - Streaming evaluation
                           # - Memory optimization
                           # - Cross-model comparison
```

### 5. **ModelSimpleTesting.py**
Interactive testing interface for real-time predictions with visual feedback.

## 📊 Evaluation Metrics

- **Accuracy**: Overall classification correctness
- **Precision**: Per-class positive prediction accuracy
- **Recall**: Per-class detection rate
- **F1-Score**: Balanced precision-recall metric
- **Confusion Matrix**: Detailed class-wise prediction analysis

## 🚀 Quick Start

### Installation
```bash
pip install -r requirements.txt
```

### Dataset Preparation
```python
from DatasetPreparation import CopySplitDataFromDir

CopySplitDataFromDir(
    source_dir="path/to/intel-image-dataset",
    output_dir="Datasets/Split1",
    train_ratio=0.64,
    val_ratio=0.16,
    test_ratio=0.20
)
```

### Training
```bash
python ModelTraining.py
```

Trains on all three splits and saves:
- Best models: `TrainingOutputs/SplitX/MODELX.keras`
- Checkpoints: `TrainingOutputs/SplitX/checkpoints/`
- Training history: `TrainingOutputs/SplitX/training_history.png`
- Statistics: `TrainingOutputs/SplitX/training_stats.json`

### Evaluation
```python
from EvaluateModel import evaluate_model

evaluate_model(
    model_path="./TrainingOutputs/Split1/MODEL1.keras",
    test_dir="./Datasets/Split1/test",
    result_dir="Split1",
    img_size=(128, 128)
)
```

### Multi-Model Comparison
```python
from ModelTesting import MultiModelSplit1Evaluator

evaluator = MultiModelSplit1Evaluator(
    model_paths={
        "Model1": "./TrainingOutputs/Split1/MODEL1.keras",
        "Model2": "./TrainingOutputs/Split2/MODEL2.keras",
        "Model3": "./TrainingOutputs/Split3/MODEL3.keras"
    },
    class_names=["buildings", "forest", "glacier", "mountain", "sea", "street"]
)

results = evaluator.evaluate_all({
    "train": "./Datasets/Split1/train",
    "val": "./Datasets/Split1/val",
    "test": "./Datasets/Split1/test"
})
```

## 📁 Directory Structure

```
Deep Learning in Computer Vision/
├── DatasetPreparation.py     # Dataset handling and augmentation
├── ModelTraining.py          # Model architecture and training
├── EvaluateModel.py          # Single model evaluation
├── ModelTesting.py           # Multi-model comparison
├── ModelSimpleTesting.py     # Interactive testing
├── requirements.txt          # Dependencies
├── Datasets/                 # Dataset splits
│   ├── Split1/
│   ├── Split2/
│   └── Split3/
└── TrainingOutputs/          # Trained models and checkpoints
    ├── Split1/
    ├── Split2/
    └── Split3/
```

## 📦 Prerequisites

- Python 3.8+
- TensorFlow 2.18+ (or tf-nightly for RTX 50 series)
- NumPy, Pandas, Matplotlib
- Scikit-learn, Seaborn
- GPU support recommended (CUDA-capable GPU with 8GB+ VRAM)

## 🎓 Learning Outcomes

- Deep CNN architecture design and implementation
- Image preprocessing, normalization, and augmentation
- Training strategies (early stopping, checkpointing, monitoring)
- Comprehensive model evaluation and comparison
- Memory-efficient deep learning inference
- Multi-dataset validation for robustness

## 📘 References

- **Dataset**: [Intel Image Classification - Kaggle](https://www.kaggle.com/datasets/puneet6060/intel-image-classification)
- **Base Project**: Systems with Machine Learning
- **Frameworks**: TensorFlow, Keras 3.9.2+

---

*Deep learning practical application emphasizing robust evaluation methodologies and systematic accuracy improvement techniques.*
