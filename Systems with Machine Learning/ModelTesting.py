import os
import numpy as np
import json
from sklearn.metrics import classification_report, confusion_matrix
import tensorflow as tf
from DatasetPreparation import LoadDatasetWithNormalization
import gc
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from tqdm import tqdm
import time


class MultiModelSplit1Evaluator:
    def __init__(self, model_paths, class_names):
        self.models = {}
        self.class_names = class_names
        self.num_classes = len(class_names)

        gpus = tf.config.experimental.list_physical_devices('GPU')
        if gpus:
            try:
                for gpu in gpus:
                    tf.config.experimental.set_memory_growth(gpu, True)
                    tf.config.experimental.set_virtual_device_configuration(
                        gpu, [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=2048)]
                    )
            except RuntimeError as e:
                print(f"GPU configuration error: {e}")

        print("\nLoading models...")
        for name, path in model_paths.items():
            if os.path.exists(path):
                self.models[name] = tf.keras.models.load_model(path)
                print(f"Loaded {name}")
            else:
                print(f"Warning: {path} not found!")

    def safe_convert_to_numpy(self, x):
        if isinstance(x, np.ndarray):
            return x
        elif hasattr(x, 'numpy'):
            return x.numpy()
        else:
            return np.array(x)

    def evaluate_model_streaming(self, model_name, model, dataset_path, dataset_type, batch_size=4,
                                 img_size=(128, 128)):
        print(f"\nEvaluating {model_name} on {dataset_type} data...")

        try:
            dataset = LoadDatasetWithNormalization(dataset_path, batch_size=batch_size, target_size=img_size)

            y_true = []
            y_pred = []
            y_pred_proba = []
            processed_batches = 0
            start_time = time.time()

            pbar = tqdm(desc=f"Processing {model_name} {dataset_type}", unit="batch")

            for batch_x, batch_y in dataset:
                try:
                    batch_x_np = self.safe_convert_to_numpy(batch_x)
                    batch_y_np = self.safe_convert_to_numpy(batch_y)

                    batch_pred = model.predict(batch_x_np, batch_size=min(4, len(batch_x_np)), verbose=0)

                    y_pred.extend(np.argmax(batch_pred, axis=1))
                    y_true.extend(np.argmax(batch_y_np, axis=1))
                    y_pred_proba.extend(batch_pred)

                    processed_batches += 1
                    pbar.set_postfix({
                        'Samples': len(y_true),
                        'Batches': processed_batches
                    })
                    pbar.update(1)

                    del batch_x, batch_y, batch_x_np, batch_y_np, batch_pred
                    gc.collect()

                    if len(y_true) >= 1000:
                        print(f"Limiting to {len(y_true)} samples for memory efficiency")
                        break

                except Exception as batch_error:
                    print(f"Error in batch {processed_batches}: {batch_error}")
                    continue

            pbar.close()

            if not y_true:
                print(f"No data processed for {dataset_type}")
                return None

            y_true = np.array(y_true)
            y_pred = np.array(y_pred)
            y_pred_proba = np.array(y_pred_proba)

            accuracy = np.mean(y_pred == y_true)

            class_report = classification_report(y_true, y_pred,
                                                 target_names=self.class_names,
                                                 output_dict=True,
                                                 zero_division=0)

            conf_matrix = confusion_matrix(y_true, y_pred)

            per_class_accuracy = []
            for i in range(self.num_classes):
                class_mask = (y_true == i)
                if np.sum(class_mask) > 0:
                    class_acc = np.mean(y_pred[class_mask] == y_true[class_mask])
                    per_class_accuracy.append(class_acc)
                else:
                    per_class_accuracy.append(0.0)

            elapsed_time = time.time() - start_time
            print(
                f"{model_name} {dataset_type}: Accuracy={accuracy:.4f}, Samples={len(y_true)}, Time={elapsed_time:.2f}s")

            result = {
                'dataset_type': dataset_type,
                'accuracy': accuracy,
                'y_true': y_true,
                'y_pred': y_pred,
                'y_pred_proba': y_pred_proba,
                'classification_report': class_report,
                'confusion_matrix': conf_matrix,
                'per_class_accuracy': per_class_accuracy,
                'evaluation_time': elapsed_time,
                'samples_processed': len(y_true)
            }

            gc.collect()
            return result

        except Exception as e:
            print(f"Error evaluating {model_name} {dataset_type}: {e}")
            gc.collect()
            return None

    def evaluate_all(self, dataset_paths, batch_size=4, img_size=(128, 128)):
        all_results = {}
        for model_name, model in self.models.items():
            model_results = {}
            for dataset_type, dataset_path in dataset_paths.items():
                if os.path.exists(dataset_path):
                    print(f"\n{'=' * 50}")
                    print(f"Evaluating {model_name} on {dataset_type}")
                    print(f"{'=' * 50}")
                    result = self.evaluate_model_streaming(model_name, model, dataset_path, dataset_type, batch_size,
                                                           img_size)
                    if result is not None:
                        model_results[dataset_type] = result

                    gc.collect()
                    tf.keras.backend.clear_session()

            all_results[model_name] = model_results
        return all_results

    def create_comprehensive_visualizations(self, all_results, save_dir):
        """Create comprehensive visualizations for all models"""
        print("Creating comprehensive visualizations...")

        fig, axes = plt.subplots(len(all_results), 3, figsize=(15, 5 * len(all_results)))
        if len(all_results) == 1:
            axes = axes.reshape(1, -1)

        for row_idx, (model_name, model_results) in enumerate(all_results.items()):
            for col_idx, dataset_type in enumerate(['train', 'val', 'test']):
                ax = axes[row_idx, col_idx]
                if dataset_type in model_results:
                    result = model_results[dataset_type]
                    cm = result['confusion_matrix']
                    cm_normalized = cm.astype('float') / (cm.sum(axis=1)[:, np.newaxis] + 1e-10)

                    sns.heatmap(cm_normalized, annot=True, fmt='.2f', cmap='Blues',
                                xticklabels=self.class_names, yticklabels=self.class_names,
                                ax=ax)
                    ax.set_title(f'{model_name} - {dataset_type.upper()}\nAcc: {result["accuracy"]:.3f}')
                    ax.set_xlabel('Predicted')
                    ax.set_ylabel('Actual')
                else:
                    ax.set_title(f'{model_name} - {dataset_type.upper()}\nNo Data')
                    ax.axis('off')

        plt.tight_layout()
        plt.savefig(os.path.join(save_dir, 'confusion_matrices_all_models.png'), dpi=200, bbox_inches='tight')
        plt.close()

        fig, axes = plt.subplots(2, 2, figsize=(15, 12))

        data = []
        for model_name, model_results in all_results.items():
            for dataset_type, result in model_results.items():
                data.append({
                    'Model': model_name,
                    'Dataset': dataset_type.upper(),
                    'Accuracy': result['accuracy'],
                    'F1_Macro': result['classification_report']['macro avg']['f1-score'],
                    'F1_Weighted': result['classification_report']['weighted avg']['f1-score'],
                    'Precision': result['classification_report']['macro avg']['precision'],
                    'Recall': result['classification_report']['macro avg']['recall'],
                    'Samples': result['samples_processed'],
                    'Time': result['evaluation_time']
                })

        df = pd.DataFrame(data)

        sns.barplot(data=df, x='Dataset', y='Accuracy', hue='Model', ax=axes[0, 0])
        axes[0, 0].set_title('Accuracy Comparison Across Models and Datasets')
        axes[0, 0].set_ylim(0, 1)
        axes[0, 0].legend(title='Model')

        sns.barplot(data=df, x='Dataset', y='F1_Macro', hue='Model', ax=axes[0, 1])
        axes[0, 1].set_title('F1-Score (Macro) Comparison')
        axes[0, 1].set_ylim(0, 1)
        axes[0, 1].legend(title='Model')

        # Precision vs Recall
        sns.scatterplot(data=df, x='Precision', y='Recall', hue='Model', style='Dataset', s=100, ax=axes[1, 0])
        axes[1, 0].set_title('Precision vs Recall by Model')
        axes[1, 0].plot([0, 1], [0, 1], 'k--', alpha=0.5)
        axes[1, 0].set_xlim(0, 1)
        axes[1, 0].set_ylim(0, 1)

        # Evaluation time comparison
        sns.barplot(data=df, x='Model', y='Time', hue='Dataset', ax=axes[1, 1])
        axes[1, 1].set_title('Evaluation Time by Model')
        axes[1, 1].set_ylabel('Time (seconds)')

        plt.tight_layout()
        plt.savefig(os.path.join(save_dir, 'performance_comparison_all_models.png'), dpi=200, bbox_inches='tight')
        plt.close()

        # 3. Per-class analysis
        class_data = []
        for model_name, model_results in all_results.items():
            for dataset_type, result in model_results.items():
                for i, class_name in enumerate(self.class_names):
                    class_metrics = result['classification_report'][class_name]
                    class_data.append({
                        'Model': model_name,
                        'Dataset': dataset_type.upper(),
                        'Class': class_name,
                        'Precision': class_metrics['precision'],
                        'Recall': class_metrics['recall'],
                        'F1_Score': class_metrics['f1-score'],
                        'Support': class_metrics['support'],
                        'Per_Class_Accuracy': result['per_class_accuracy'][i]
                    })

        class_df = pd.DataFrame(class_data)

        fig, axes = plt.subplots(2, 2, figsize=(15, 12))

        test_class_data = class_df[class_df['Dataset'] == 'TEST']
        sns.boxplot(data=test_class_data, x='Class', y='Per_Class_Accuracy', hue='Model', ax=axes[0, 0])
        axes[0, 0].set_title('Per-Class Accuracy on Test Set')
        axes[0, 0].set_ylabel('Accuracy')
        axes[0, 0].tick_params(axis='x', rotation=45)

        sns.barplot(data=test_class_data, x='Class', y='F1_Score', hue='Model', ax=axes[0, 1])
        axes[0, 1].set_title('F1-Score by Class (Test Set)')
        axes[0, 1].set_ylabel('F1-Score')
        axes[0, 1].tick_params(axis='x', rotation=45)

        sns.barplot(data=test_class_data, x='Class', y='Support', hue='Model', ax=axes[1, 0])
        axes[1, 0].set_title('Class Support in Test Sets')
        axes[1, 0].set_ylabel('Number of Samples')
        axes[1, 0].tick_params(axis='x', rotation=45)

        avg_class_perf = test_class_data.groupby('Class')['Per_Class_Accuracy'].mean().sort_values(ascending=False)
        avg_class_perf.plot(kind='bar', ax=axes[1, 1], color='skyblue')
        axes[1, 1].set_title('Average Per-Class Accuracy (All Models)')
        axes[1, 1].set_ylabel('Average Accuracy')
        axes[1, 1].tick_params(axis='x', rotation=45)

        plt.tight_layout()
        plt.savefig(os.path.join(save_dir, 'per_class_analysis_all_models.png'), dpi=200, bbox_inches='tight')
        plt.close()

        plt.clf()
        plt.cla()
        gc.collect()

        return df, class_df




def main():
    """Main function for multi-model evaluation"""
    print("Starting Multi-Model Evaluation (MODEL1, MODEL2, MODEL3)...")

    model_paths = {
        'MODEL1': './TrainingOutputs/Split1/MODEL1.keras',
        'MODEL2': './TrainingOutputs/Split2/MODEL2.keras',
        'MODEL3': './TrainingOutputs/Split3/MODEL3.keras'
    }

    class_names = ['cats', 'dogs', 'horses', 'humans']

    output_dir = './MultiModel_Split1_Evaluation'
    os.makedirs(output_dir, exist_ok=True)

    evaluator = MultiModelSplit1Evaluator(model_paths, class_names)

    if not evaluator.models:
        print("No models loaded successfully!")
        return

    split1_datasets = {
        'train': './Split1/train',
        'val': './Split1/val',
        'test': './Split1/test'
    }

    # Run evaluation
    print(f"\nEvaluating {len(evaluator.models)} models on Split1 datasets...")
    total_start_time = time.time()

    all_results = evaluator.evaluate_all(split1_datasets, batch_size=4)

    total_time = time.time() - total_start_time

    for model_name, results in all_results.items():
        for dataset_type, result in results.items():
            with open(os.path.join(output_dir, f'{model_name}_{dataset_type}_results.json'), 'w') as f:
                json.dump({
                    'model': model_name,
                    'dataset': f'Split1/{dataset_type}',
                    'accuracy': float(result['accuracy']),
                    'f1_macro': float(result['classification_report']['macro avg']['f1-score']),
                    'f1_weighted': float(result['classification_report']['weighted avg']['f1-score']),
                    'samples_processed': int(result['samples_processed']),
                    'evaluation_time': float(result['evaluation_time']),
                    'per_class_metrics': {
                        class_name: {
                            'precision': float(result['classification_report'][class_name]['precision']),
                            'recall': float(result['classification_report'][class_name]['recall']),
                            'f1_score': float(result['classification_report'][class_name]['f1-score']),
                            'support': int(result['classification_report'][class_name]['support']),
                            'accuracy': float(result['per_class_accuracy'][i])
                        }
                        for i, class_name in enumerate(class_names)
                    }
                }, f, indent=2)

    if all_results:
        print(f"\nCreating comprehensive analysis and visualizations...")

        performance_df, class_df = evaluator.create_comprehensive_visualizations(all_results, output_dir)

        with open(os.path.join(output_dir, 'all_models_comprehensive_results.json'), 'w') as f:
            json.dump({
                'evaluation_summary': {
                    model_name: {
                        dataset_type: {
                            'accuracy': float(result['accuracy']),
                            'f1_macro': float(result['classification_report']['macro avg']['f1-score']),
                            'samples': int(result['samples_processed']),
                            'time': float(result['evaluation_time'])
                        }
                        for dataset_type, result in model_results.items()
                    }
                    for model_name, model_results in all_results.items()
                },
                'class_names': class_names,
                'total_evaluation_time': total_time,
                'models_evaluated': list(all_results.keys())
            }, f, indent=2)

        if not performance_df.empty:
            performance_df.to_csv(os.path.join(output_dir, 'multi_model_performance_summary.csv'), index=False)
        if not class_df.empty:
            class_df.to_csv(os.path.join(output_dir, 'multi_model_class_analysis.csv'), index=False)

        print(f"\nMulti-model evaluation completed!")
        print(f"Results saved in: {output_dir}")
        print(f"Total time: {total_time:.2f} seconds")
        print(f"Models evaluated: {', '.join(all_results.keys())}")

        print(f"\nFINAL SUMMARY:")
        for model_name, model_results in all_results.items():
            print(f"\n{model_name}:")
            for dataset_type, result in model_results.items():
                acc = result['accuracy']
                f1 = result['classification_report']['macro avg']['f1-score']
                samples = result['samples_processed']
                print(f"  {dataset_type.upper()}: Acc={acc:.4f}, F1={f1:.4f}, Samples={samples}")

        # Best model identification
        if not performance_df.empty:
            test_data = performance_df[performance_df['Dataset'] == 'TEST']
            if not test_data.empty:
                best_model = test_data.loc[test_data['Accuracy'].idxmax(), 'Model']
                best_accuracy = test_data['Accuracy'].max()
                print(f"\nBEST MODEL: {best_model} (Test Accuracy: {best_accuracy:.4f})")


    else:
        print("No results generated.")


if __name__ == "__main__":
    main()
