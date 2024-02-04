import torch
import json

class classifyModel(object):
    def __init__(self):
        pass
    def forward(self, graph):
        node_num = len(graph.nodes())
        output = torch.randint(0,2,size=(node_num,))
        
        return output.tolist()