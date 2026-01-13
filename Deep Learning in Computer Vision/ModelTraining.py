import os
# Suppress TensorFlow logs BEFORE importing
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import time
import matplotlib.pyplot as plt
import numpy as np
import json

import tensorflow as tf
import logging
logging.getLogger('tensorflow').setLevel(logging.ERROR)

# Configure GPU memory growth
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        print(f"GPU enabled: {gpus[0].name}")
    except RuntimeError as e:
        print(f"GPU configuration error: {e}")
else:
    print("No GPU found - running on CPU")

from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, Input
from keras.callbacks import ModelCheckpoint, EarlyStopping
from DatasetPreparation import LoadDatasetWithNormalization


def CreateModel(input_shape=(128, 128, 3), num_classes=4):

    model = Sequential([
        Input(shape=input_shape),
        Conv2D(64, (3, 3), activation='relu', padding='same'),
        MaxPooling2D(2, 2),

        Conv2D(128, (3, 3), activation='relu', padding='same'),
        MaxPooling2D(2, 2),

        Conv2D(256, (3, 3), activation='relu', padding='same'),
        MaxPooling2D(2, 2),

        Conv2D(512, (3, 3), activation='relu', padding='same'),
        MaxPooling2D(2, 2),

        Flatten(),
        Dense(512, activation='relu'),
        Dropout(0.5),
        Dense(num_classes, activation='softmax')
    ])

    optimizer = tf.keras.optimizers.Adam(learning_rate=1e-4)
    model.compile(
        optimizer=optimizer,
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    return model

def TrainAndEvaluate(split_dir, output_dir, batch_size=32, epochs=30, img_size=(128, 128)):
    os.makedirs(output_dir, exist_ok=True)
    checkpoint_dir = os.path.join(output_dir, 'checkpoints')
    os.makedirs(checkpoint_dir, exist_ok=True)
    
    train_dir = os.path.join(split_dir, 'train')
    val_dir = os.path.join(split_dir, 'val')
    
    start_time = time.time()
    
    train_dataset = LoadDatasetWithNormalization(train_dir, batch_size=batch_size, target_size=img_size)
    val_dataset = LoadDatasetWithNormalization(val_dir, batch_size=batch_size, target_size=img_size)
    
    num_classes = len(train_dataset.class_indices)
    print(f"Found {num_classes} classes: {train_dataset.class_indices}")
    
    model = CreateModel(input_shape=(img_size[0], img_size[1], 3), num_classes=num_classes)
    model.summary()
    
    checkpoint_path = os.path.join(checkpoint_dir, 'model_checkpoint_{epoch:02d}_{val_accuracy:.4f}.keras')
    
    #creating model checkpoints every time validation accuracy is better than before
    callbacks = [
        ModelCheckpoint(
            filepath=checkpoint_path,
            save_best_only=True,
            monitor='val_accuracy',
            mode='max',
            save_weights_only=False,
            verbose=1
        )
    ]
    
    callbacks.append(
        EarlyStopping(
            monitor='val_accuracy',
            patience=10,
            restore_best_weights=True,
            verbose=1
        )
    )
        
    
    history = model.fit(
        train_dataset,
        epochs=epochs,
        validation_data=val_dataset,
        callbacks=callbacks
    )
    
    training_time = time.time() - start_time
    
    stats = { #future notice - add stats from checkpoints as well
        'training_time_seconds': training_time,
        'epochs_completed': len(history.history['loss']),
        'final_training_loss': history.history['loss'][-1],
        'final_training_accuracy': history.history['accuracy'][-1],
        'final_validation_loss': history.history['val_loss'][-1],
        'final_validation_accuracy': history.history['val_accuracy'][-1],
        'best_validation_accuracy': max(history.history['val_accuracy']),
        'best_validation_epoch': np.argmax(history.history['val_accuracy']) + 1
    }
    
    return model, history, stats

def GeneratePlot(history, save_path=None):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    
    #plot for accuracy
    ax1.plot(history.history['accuracy'], label='Training Accuracy')
    ax1.plot(history.history['val_accuracy'], label='Validation Accuracy')
    ax1.set_title('Model Accuracy')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Accuracy')
    ax1.legend()
    ax1.grid(True)
    
    #plot for loss
    ax2.plot(history.history['loss'], label='Training Loss')
    ax2.plot(history.history['val_loss'], label='Validation Loss')
    ax2.set_title('Model Loss')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Loss')
    ax2.legend()
    ax2.grid(True)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path)
        plt.close()
    else:
        plt.show()

def FindBestModel(checkpoint_dir): #validation accuracy
    checkpoint_files = [f for f in os.listdir(checkpoint_dir) if f.endswith('.keras')]
    
    if not checkpoint_files:
        return None
    
    val_accuracies = []
    for f in checkpoint_files:
        try:
            val_acc = float(f.split('_')[-1].replace('.keras', ''))
            val_accuracies.append((f, val_acc))
        except:
            continue
    
    if val_accuracies:
        best_model_file, best_acc = max(val_accuracies, key=lambda x: x[1])
        return os.path.join(checkpoint_dir, best_model_file), best_acc
    
    return None, 0.0


def TrainSplit(split_name, output_model_path, batch_size=32, epochs=30, img_size=(128, 128)):
    split_dir = f'./Datasets/{split_name}'
    output_dir = f'./TrainingOutputs/{split_name}'
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\nTraining on {split_name}...")
    
    model, history, stats = TrainAndEvaluate(
        split_dir=split_dir,
        output_dir=output_dir,
        batch_size=batch_size,
        epochs=epochs,
        img_size=img_size,
    )
    
    for key, value in stats.items():
        if isinstance(value, (np.int64, np.int32, np.int16, np.int8)):
            stats[key] = int(value)
        elif isinstance(value, (np.float64, np.float32)):
            stats[key] = float(value)
    
    GeneratePlot(history, save_path=os.path.join(output_dir, 'training_history.png'))
    
    checkpoint_dir = os.path.join(output_dir, 'checkpoints')
    best_model_path, best_acc = FindBestModel(checkpoint_dir)
    
    if best_model_path:
        best_model = tf.keras.models.load_model(best_model_path)
        best_model.save(output_model_path)
        print(f"Best model saved to {output_model_path} (val_acc: {best_acc:.4f})")
        
        stats['best_model_path'] = best_model_path
        stats['best_model_val_accuracy'] = best_acc
    else:
        print("Could not find best model checkpoint.")
    
    with open(os.path.join(output_dir, 'training_stats.json'), 'w') as f:
        json.dump(stats, f, indent=4)
    
    print(f"{split_name} training completed in {stats['training_time_seconds']:.2f} seconds")
    print(f"Best validation accuracy: {stats['best_validation_accuracy']:.4f} (epoch {stats['best_validation_epoch']})")
    print(f"Final training accuracy: {stats['final_training_accuracy']:.4f}")
    print(f"Final validation accuracy: {stats['final_validation_accuracy']:.4f}")

# ------------------------------------------------------- RUN ------------------------------------------------------------

if __name__ == "__main__":
    os.makedirs('./TrainingOutputs', exist_ok=True)
    
    # Split1
    # TrainSplit(
    #     split_name='Split1',
    #     output_model_path='./TrainingOutputs/Split1/MODEL1.keras',
    #     batch_size=128,
    #     epochs=50,
    #     img_size=(128, 128),
    # )
    
    # Split2
    # TrainSplit(
    #     split_name='Split2',
    #     output_model_path='./TrainingOutputs/Split2/MODEL2.keras',
    #     batch_size=128,
    #     epochs=50,
    #     img_size=(128, 128),
    # )

    # Split3
    TrainSplit(
        split_name='Split3',
        output_model_path='./TrainingOutputs/Split3/MODEL3.keras',
        batch_size=128,
        epochs=50,
        img_size=(150, 150),
    )
    
    print("\nAll training completed successfully!")