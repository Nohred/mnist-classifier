from torch import nn

class MLP(nn.Module):
    # MLP hereda de nn.Module para aprovechar las funcionalidades de PyTorch
    def __init__(self, input_size, hidden_size, output_size):
        super(MLP, self).__init__() # Llamada al constructor de la clase padre
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, output_size)
        self.dp = nn.Dropout(p=0.4)
        self.relu = nn.ReLU()
    
    def forward(self, x):
        x = x.view(x.size(0), -1)
        # aplanar la imagen para que sea un vector
        x = self.fc1(x)
        x = self.relu(x)
        x = self.dp(x)
        x = self.fc2(x)
        return x
    
    




"""

class MLP(nn.Module):
    # MLP hereda de nn.Module para aprovechar las funcionalidades de PyTorch
    def __init__(self, input_size, hidden_size, output_size):
        super(MLP, self).__init__() # Llamada al constructor de la clase padre
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, output_size)
        self.dp = nn.Dropout(p=0.2)
        self.sigmoid = nn.Sigmoid()
    
    def forward(self, x):
        x = self.fc1(x)
        x = self.sigmoid(x)
        x = self.dp(x)
        x = self.fc2(x)
        # x = self.sigmoid(x)

        return x
"""
