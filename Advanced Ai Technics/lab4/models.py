import torch
import torch.nn.functional as F
from torch_geometric.nn import GCNConv, GATConv

class MLP(torch.nn.Module):
    def __init__(self, in_channels, out_channels, num_layers, activation, **kwargs):
        # *args is used to match the function signature of GAT
        super().__init__()
        hidden_channels = None # <--
        self.layers = torch.nn.ModuleList()
        self.layers.append(torch.nn.Linear()) # <--
        for _ in range(num_layers - 2):
            self.layers.append(torch.nn.Linear())# <--
        self.layers.append(torch.nn.Linear())# <--
        self.activation = activation

    def forward(self, x, edge_index=None):
        for layer in self.layers[:-1]:
            x = self.activation(layer(x))
        return self.layers[-1](x)

class GCN(torch.nn.Module):
    def __init__(self, in_channels, out_channels, num_layers, activation, **kwargs):
        # *args is used to match the function signature of GAT
        super().__init__()
        hidden_channels = None # <--
        self.layers = torch.nn.ModuleList()
        self.layers.append(GCNConv())# <--
        for _ in range(num_layers - 2):
            self.layers.append(GCNConv())# <--
        self.layers.append(GCNConv())# <--
        self.activation = activation

    def forward(self, x, edge_index):
        for conv in self.layers[:-1]:
            x = self.activation(conv(x, edge_index))
        return self.layers[-1](x, edge_index)

class GAT(torch.nn.Module):
    def __init__(self, in_channels, out_channels, num_layers, activation, heads):
        super().__init__()
        hidden_channels = None # <--
        head_channels = None # <--
        self.layers = torch.nn.ModuleList()
        self.layers.append(GATConv())# <--
        for _ in range(num_layers - 2):
            self.layers.append(GATConv())# <--
        self.layers.append(GATConv())# <--
        self.activation = activation

    def forward(self, x, edge_index):
        for conv in self.layers[:-1]:
            x = self.activation(conv(x, edge_index))
        return self.layers[-1](x, edge_index)

if __name__ == "__main__":
    ## print number of parameters in each model
    in_channels = 1433
    out_channels = 7
    num_layers = 3
    activation = torch.relu
    heads = 4
    mlp = MLP(in_channels, out_channels, num_layers, activation)
    gcn = GCN(in_channels, out_channels, num_layers, activation)
    gat = GAT(in_channels, out_channels, num_layers, activation, heads)
    
    # test for random data
    x = torch.randn(1, in_channels)
    edge_index = torch.randint(0, 1, (2, 1))
    mlp(x)
    gcn(x, edge_index)
    gat(x, edge_index)
    # print number of parameters in each model
    
    print(f"MLP parameters: {sum(p.numel() for p in mlp.parameters())}")
    print(f"GCN parameters: {sum(p.numel() for p in gcn.parameters())}")
    print(f"GAT parameters: {sum(p.numel() for p in gat.parameters())}")



