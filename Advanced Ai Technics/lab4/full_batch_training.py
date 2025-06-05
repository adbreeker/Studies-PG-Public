import time
import torch
from data_processing import load_data
from models import MLP, GCN, GAT

def train(model, data, optimizer, criterion):
    model.train()
    optimizer.zero_grad()
    out = model(data.x, data.edge_index)
    loss = criterion(out[data.train_mask], data.y[data.train_mask])
    loss.backward()
    optimizer.step()
    return loss.item()

def test(model, data):
    model.eval()
    out = model(data.x, data.edge_index)
    pred = out.argmax(dim=1)
    acc = (pred[data.test_mask] == data.y[data.test_mask]).sum().item() / data.test_mask.sum().item()
    return acc

def run_training(model_class):
    data = load_data()
    model = model_class(data.num_node_features, data.num_classes, num_layers=3, activation=torch.relu, heads=4)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    criterion = torch.nn.CrossEntropyLoss()

    time_start = time.time()
    for epoch in range(3):
        train(model, data, optimizer, criterion)
    total_time = time.time() - time_start

    acc = test(model, data)
    print(f"{model_class.__name__} Training time for 3 epochs (full batch): {total_time:.4f} seconds")
    print(f"{model_class.__name__} Accuracy after 3 epochs (full batch): {acc:.4f}")

if __name__ == "__main__":
    for model_class in [MLP, GCN, GAT]:
        run_training(model_class)
