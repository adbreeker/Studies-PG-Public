import time
import torch
from torch_geometric.loader import NeighborLoader
from data_processing import load_data
from models import GCN, GAT, MLP

def test(model, data):
    model.eval()
    out = model(data.x, data.edge_index)
    pred = out.argmax(dim=1)
    acc = (pred[data.test_mask] == data.y[data.test_mask]).sum().item() / data.test_mask.sum().item()
    return acc

def run_sampled_training(train_time):
    data = load_data()

    # Common model settings 
    num_layers = 3
    activation = torch.relu
    model_classes = {
        "GCN": GCN,
        "GAT": GAT,
        "MLP": MLP,
    }

    for model_name, ModelClass in model_classes.items():
        print(f"\n--- Training {model_name} with sampling ---")

        # Create model
        model = ModelClass(
            in_channels=data.num_node_features, 
            out_channels=data.num_classes,
            num_layers=num_layers,
            activation=activation,
            heads=4 if model_name == "GAT" else None,
        )

        # Define NeighborLoader for sampling
        loader = NeighborLoader(
            data,
            input_nodes=data.train_mask,
            num_neighbors=[15, 10, 5],  # 3-layer neighborhood
            batch_size=32,
            shuffle=True
        )

        optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
        criterion = torch.nn.CrossEntropyLoss()

        model.train()
        start = time.time()

        stop_training = False
        n_iters = 0
        while not stop_training:
            for batch in loader: 
                optimizer.zero_grad()
                out = model(batch.x, batch.edge_index)

                # Only compute loss on original target nodes (first batch_size entries)
                loss = criterion(out[:batch.batch_size], batch.y[:batch.batch_size])
                loss.backward()

                elapsed = time.time() - start
                if elapsed > train_time[model_name]:
                    stop_training = True
                    break  # Exit early before optimizer step

                optimizer.step() 
                n_iters += 1

        acc = test(model, data)
        print(f"{model_name} Training time for {n_iters} iterations (sampling): {elapsed:.4f} seconds")
        print(f"{model_name} Accuracy after {n_iters} iterations (sampling): {acc:.4f}")

if __name__ == "__main__":
    train_time = {"GCN": 0.0, "GAT": 0.0, "MLP": 0.0}  # <--
    run_sampled_training(train_time)
