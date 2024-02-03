import os
import json
import argparse	
import subprocess
import networkx as nx
from copy import deepcopy
from slither.slither import Slither

from graph.callGraphUtils import GESCPrinters

'''获取完整call图'''
def generate_cg_graph(sol_file_name, sol_file_path, version):
  
       
    # 设置为当前版本
    command = f"solc-select use {version}"
    subprocess.run(command, shell=True)
    # 使用slither解析
    slither = Slither(sol_file_path)
    # 获取文件全部漏洞信息
    list_sol_file_vul_info = None

    # 初始化call生成器类
    call_graph_printer = GESCPrinters(slither, None)
    # 生成call图
    file_call_graph = call_graph_printer.generate_call_graph(sol_file_name, list_sol_file_vul_info)

    return file_call_graph
