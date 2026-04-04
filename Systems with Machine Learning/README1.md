# Systems with Machine Learning (SzUM) 🤖

This repository contains a comprehensive implementation of a deep learning image classification system using Convolutional Neural Networks with TensorFlow and Keras. The project demonstrates end-to-end machine learning workflow including data preprocessing, model training, evaluation, and testing across multiple data splits.

## 🎯 Project Objectives

- Develop and train deep CNN architectures for multi-class image classification
- Implement robust data preprocessing and augmentation pipelines
- Perform comprehensive model evaluation with statistical analysis
- Compare performance across different data splits and validation strategies
- Apply best practices for machine learning model development and testing

## 🏗️ System Architecture

### Model Architecture
The system implements a deep Convolutional Neural Network with the following structure:

```
Input (128x128x3)
    ↓
Conv2D(64) → MaxPool → Conv2D(128) → MaxPool
    ↓
Conv2D(256) → MaxPool → Conv2D(512) → MaxPool
    ↓
Flatten → Dense(512) → Dropout(0.5) → Dense(4)
    ↓
Softmax Classification
```

### Data Pipeline
- **Dataset Splitting**: Configurable train/validation/test splits (64%/16%/20%)
- **Data Augmentation**: Rotation, zoom, shift, flip, brightness adjustments
- **Normalization**: Image standardization and preprocessing
- **Multi-Split Validation**: Three different data splitting strategies for robust evaluation

## 📋 Prerequisites

### Software Requirements
- Python 3.8+
- TensorFlow 2.19.0
- Keras 3.9.2
- NumPy, Pandas, Matplotlib
- Scikit-learn for evaluation metrics
- Seaborn for visualization

### Hardware Requirements
- GPU support recommended (CUDA-capable)
- Minimum 8GB RAM
- Storage space for dataset and model checkpoints

## 🚀 Getting Started

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd "Systems with Machine Learning"
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Quick Start

1. **Prepare your dataset**
   ```python
   from DatasetPreparation import CopySplitDataFromDir
   
   # Split dataset into train/val/test
   CopySplitDataFromDir(
       source_dir="path/to/original/dataset",
       output_dir="Split1",
       train_ratio=0.64,
       val_ratio=0.16,
       test_ratio=0.20
   )
   ```

2. **Train the model**
   ```bash
   python ModelTraining.py
   ```

3. **Evaluate the model**
   ```bash
   python EvaluateModel.py
   ```

4. **Interactive testing**
   ```bash
   python ModelSimpleTesting.py
   ```

## 🔧 Core Components

### 1. Data Preparation (`DatasetPreparation.py`)
- **Splitting Functions**: Automated dataset partitioning
- **Augmentation Pipeline**: Image transformation and enhancement
- **Cross-Split Generation**: Multiple validation strategies
- **Normalization**: Consistent image preprocessing

### 2. Model Training (`ModelTraining.py`)
- **CNN Architecture**: Deep convolutional network implementation
- **Training Loop**: Configurable epochs, batch size, learning rate
- **Checkpointing**: Best model saving based on validation accuracy
- **Early Stopping**: Prevent overfitting with patience mechanism
- **Visualization**: Training history plots and metrics

### 3. Model Evaluation (`EvaluateModel.py`)
- **Performance Metrics**: Accuracy, precision, recall, F1-score
- **Confusion Matrix**: Class-wise prediction analysis
- **Classification Reports**: Detailed per-class statistics
- **Visualization**: Heatmaps and performance charts

### 4. Advanced Testing (`ModelTesting.py`)
- **Multi-Model Comparison**: Evaluate multiple trained models
- **Cross-Split Validation**: Performance across different data splits
- **Memory Management**: Efficient GPU utilization
- **Comprehensive Analytics**: Statistical analysis and visualization

### 5. Interactive Testing (`ModelSimpleTesting.py`)
- **Real-time Prediction**: Interactive model testing interface
- **Visual Feedback**: Image display with predictions
- **User Interface**: Button-based navigation system

## 🧪 Training Process

### Model Configuration
- **Input Shape**: 128×128×3 RGB images
- **Classes**: 4-class classification problem
- **Optimizer**: Adam with learning rate 1e-4
- **Loss Function**: Categorical crossentropy
- **Metrics**: Accuracy tracking

### Training Strategy
- **Batch Size**: 32 (configurable)
- **Epochs**: 30 (with early stopping)
- **Validation**: Real-time monitoring
- **Checkpointing**: Save best performing models
- **Data Augmentation**: Applied to training set only

## 📊 Evaluation Metrics

### Performance Indicators
- **Accuracy**: Overall classification performance
- **Precision**: Class-specific positive prediction accuracy
- **Recall**: Class-specific detection rate
- **F1-Score**: Harmonic mean of precision and recall
- **Confusion Matrix**: Detailed prediction analysis

### Validation Strategy
- **Split 1**: Standard random split (64/16/20)
- **Split 2**: Alternative random configuration
- **Split 3**: Validation overlap with training (overfitting test)

## 🔄 Workflow

1. **Data Preparation**
   - Load and organize dataset
   - Split into train/validation/test sets
   - Apply augmentation to training data
   - Normalize and standardize images

2. **Model Training**
   - Initialize CNN architecture
   - Configure training parameters
   - Train with validation monitoring
   - Save best model checkpoints

3. **Evaluation**
   - Load trained models
   - Evaluate on test datasets
   - Generate performance reports
   - Create visualization plots

4. **Testing & Analysis**
   - Interactive model testing
   - Multi-model comparison
   - Statistical analysis
   - Performance optimization

## 📈 Results & Analysis

The project implements comprehensive evaluation across multiple data splits:

- **Cross-Split Validation**: Ensures model generalization
- **Overfitting Detection**: Split 3 validation strategy
- **Performance Comparison**: Multi-model statistical analysis
- **Visual Analysis**: Confusion matrices and performance plots

## 🛠️ Configuration Options

### Training Parameters
```python
# Model configuration
img_size = (128, 128)
batch_size = 32
epochs = 30
num_classes = 4

# Data split ratios
train_ratio = 0.64
val_ratio = 0.16
test_ratio = 0.20
```

### Augmentation Settings
```python
# Training augmentation
rotation_range = 20
zoom_range = 0.15
width_shift_range = [-10, 10]
height_shift_range = [-10, 10]
horizontal_flip = True
vertical_flip = True
brightness_range = [0.5, 2.0]
```

## 📝 Usage Examples

### Basic Training
```python
from ModelTraining import TrainSplit

# Train model on Split 1
TrainSplit(
    split_name="Split1",
    output_model_path="./TrainingOutputs/Split1/MODEL1.keras",
    batch_size=32,
    epochs=30
)
```

### Model Evaluation
```python
from EvaluateModel import evaluate_model

# Evaluate trained model
evaluate_model(
    model_path="./TrainingOutputs/Split1/MODEL1.keras",
    test_dir="./Split1/test",
    result_dir="Split1",
    img_size=(128, 128)
)
```

### Multi-Model Comparison
```python
from ModelTesting import MultiModelSplit1Evaluator

# Compare multiple models
evaluator = MultiModelSplit1Evaluator(
    model_paths={
        "Model1": "./TrainingOutputs/Split1/MODEL1.keras",
        "Model2": "./TrainingOutputs/Split2/MODEL2.keras",
        "Model3": "./TrainingOutputs/Split3/MODEL3.keras"
    },
    class_names=["class1", "class2", "class3", "class4"]
)

results = evaluator.evaluate_all({
    "train": "./Split1/train",
    "val": "./Split1/val",
    "test": "./Split1/test"
})
```

## 🚀 Advanced Features

### Memory Optimization
- GPU memory growth configuration
- Garbage collection between evaluations
- Batch processing for large datasets
- Virtual device memory limits

### Visualization Tools
- Training history plots
- Confusion matrix heatmaps
- Performance comparison charts
- Interactive prediction interface

### Robust Evaluation
- Streaming dataset processing
- Error handling and recovery
- Progress tracking with tqdm
- Comprehensive logging

## 📚 Documentation

- **Detailed Report**: See `SzUM-Raport_Merged.pdf` for comprehensive analysis
- **Code Documentation**: Inline comments and docstrings
- **API Reference**: Function signatures and parameter descriptions

## 🎓 Learning Outcomes

Through this project, students gain experience in:

- **Deep Learning**: CNN architecture design and implementation
- **Computer Vision**: Image preprocessing and classification
- **Model Evaluation**: Comprehensive performance analysis
- **MLOps Practices**: Model training, validation, and deployment
- **Scientific Computing**: Statistical analysis and visualization
- **Software Engineering**: Modular code design and documentation

## 👥 Team

**Project developed with:**
- [@PawelManczak](https://github.com/PawelManczak)
- [@matowaty](https://github.com/matowaty)

---

*This project demonstrates practical application of deep learning techniques for image classification, emphasizing robust evaluation methodologies and comprehensive performance analysis.*
