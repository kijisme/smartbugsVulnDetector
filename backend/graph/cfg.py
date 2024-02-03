# 构建全局异构图
import os
import json
import argparse	
import subprocess
import networkx as nx
from copy import deepcopy
from slither.slither import Slither
from slither.core.cfg.node import NodeType

'''获取一种漏洞的完整图'''
def generate_cfg_graph(sol_file_name, sol_file_path, version):

    # 设置为当前版本
    command = f"solc-select use {version}"
    subprocess.run(command, shell=True)
    
    # 使用slither解析
    slither = Slither(sol_file_path)
    # 获取文件全部漏洞信息
    list_sol_file_vul_info = None
    # 提取单个文件图
    sol_file_graph = None
    for contract in slither.contracts:
        # 初始化合约图
        contract_graph = nx.MultiDiGraph()
        # 添加状态变量节点
        for state_var in contract.state_variables:
            node_token = '_'.join([str(sol_file_name),
                                    str(contract.name),
                                    str(state_var.full_name)])
            
            node_code_lines = state_var.source_mapping.lines
            node_vuln_info = None
            contract_graph.add_node(f'{contract.name}_{state_var.full_name}',
                                    node_type='STATEVARIABLE', 
                                    node_expression=state_var.full_name,
                                    node_token=node_token,
                                    node_code_lines=node_code_lines,
                                    node_vuln_info=node_vuln_info,
                                    function_fullname=None,
                                    contract_name=contract.name, 
                                    source_file=sol_file_name)
            
        for function in contract.functions + contract.modifiers:
            
            if function.contract_declarer.name != contract.name:
                # 继承的私有函数不属于当前合约
                if function.visibility == 'private':
                    continue

            # 存储函数状态变量使用情况
            state_var_use = {}
            # 局部变量字典
            local_var_dict = {}
            # 初始化函数图
            func_graph =  nx.MultiDiGraph()
            
            for node in function.nodes:

                # 存数使用到的局部变量
                node_local_var = []

                # 获取节点信息
                node_type, node_expression, node_token, node_code_lines, node_vuln_info = get_node_info(node, list_sol_file_vul_info)
                # 添加节点    
                func_graph.add_node(node.node_id,
                                    node_type=node_type,
                                    node_expression=node_expression,
                                    node_token=node_token,
                                    node_code_lines=node_code_lines,
                                    node_vuln_info=node_vuln_info,
                                    function_fullname=function.full_name,
                                    contract_name=contract.name, 
                                    source_file=sol_file_name)
                    # 判断节点类型
                if node.type == NodeType.VARIABLE:
                    # 添加局部变量声明
                    local_var_name = node._variable_declaration
                    local_var_dict[local_var_name] = node.node_id
                else:
                    # 添加局部变量使用
                    if (node.local_variables_read + node.local_variables_written):
                        node_local_var = [x for x in (node.local_variables_read + node.local_variables_written)]

                    # 添加状态变量
                    for state_var in (function.state_variables_read + function.state_variables_written):
                        if state_var not in state_var_use.keys():
                            state_var_use[state_var] = [node.node_id]
                        else:
                            state_var_use[state_var].append(node.node_id)

                # 添加控制边
                if node.type in [NodeType.IF, NodeType.IFLOOP]:
                    true_node = node.son_true
                    if true_node:
                        if true_node.node_id not in func_graph.nodes():
                            # 获取节点信息
                            node_type, node_expression, node_token, node_code_lines, node_vuln_info = get_node_info(true_node, list_sol_file_vul_info)
                            # 添加节点    
                            func_graph.add_node(true_node.node_id,
                                                node_type=node_type,
                                                node_expression=node_expression,
                                                node_token=node_token,
                                                node_code_lines=node_code_lines,
                                                node_vuln_info=node_vuln_info,
                                                function_fullname=function.full_name,
                                                contract_name=contract.name, 
                                                source_file=sol_file_name)
                        # 添加边
                        func_graph.add_edge(node.node_id, 
                                            true_node.node_id,
                                            edge_type='if_true')

                    false_node = node.son_false
                    if false_node:
                        if false_node.node_id not in func_graph.nodes():
                            # 获取节点信息
                            node_type, node_expression, node_token, node_code_lines, node_vuln_info = get_node_info(false_node, list_sol_file_vul_info)
                            # 添加节点    
                            func_graph.add_node(false_node.node_id,
                                                node_type=node_type,
                                                node_expression=node_expression,
                                                node_token=node_token,
                                                node_code_lines=node_code_lines,
                                                node_vuln_info=node_vuln_info,
                                                function_fullname=function.full_name,
                                                contract_name=contract.name, 
                                                source_file=sol_file_name)
                        # 添加边
                        func_graph.add_edge(node.node_id, 
                                            false_node.node_id,
                                            edge_type='if_false')
                # 添加顺序边
                else:
                    for son_node in node.sons:
                        if son_node.node_id not in func_graph.nodes():
                            # 获取节点信息
                            node_type, node_expression, node_token, node_code_lines, node_vuln_info = get_node_info(son_node, list_sol_file_vul_info)
                            # 添加节点    
                            func_graph.add_node(son_node.node_id,
                                                node_type=node_type,
                                                node_expression=node_expression,
                                                node_token=node_token,
                                                node_code_lines=node_code_lines,
                                                node_vuln_info=node_vuln_info,
                                                function_fullname=function.full_name,
                                                contract_name=contract.name, 
                                                source_file=sol_file_name)
                        # 添加边
                        func_graph.add_edge(node.node_id,
                                            son_node.node_id,
                                            edge_type='next')
                
                # 添加函数局部变量数据边
                for local_var in node_local_var:
                    if local_var in local_var_dict.keys():
                        func_graph.add_edge(local_var_dict[local_var],
                                            node.node_id,
                                            edge_type='use')
                
            if len(func_graph.nodes) != 0:
                # 添加函数名称
                func_graph = nx.relabel_nodes(func_graph,  \
                            lambda x: f'{contract.name}_{function.full_name}_{str(x)}', copy=False)

            # 添加函数节点
            function_node_token = '_'.join([str(sol_file_name),
                                            str(contract.name),
                                            str(function.full_name)])
            
            function_node_code_lines = function.source_mapping.lines
            function_node_vuln_info = None
            func_graph.add_node(f'{contract.name}_{function.full_name}',
                                node_type='FUNCTION',
                                node_expression=function.full_name,
                                node_token=function_node_token,
                                node_code_lines=function_node_code_lines,
                                node_vuln_info=function_node_vuln_info,
                                function_fullname=function.full_name,
                                contract_name=contract.name, 
                                source_file=sol_file_name)
            # 添加函数边
            if f'{contract.name}_{function.full_name}_0' in func_graph.nodes():
                func_graph.add_edge(f'{contract.name}_{function.full_name}', f'{contract.name}_{function.full_name}_0', edge_type='next')
            
            # 合并图
            contract_graph = nx.compose(contract_graph, func_graph)
            
            # 添加全局数据边
            for state_var in state_var_use:
                if (state_var in contract.state_variables) or state_var.visibility != 'private':
                    for node_id in state_var_use[state_var]:
                        contract_graph.add_edge(f'{contract.name}_{state_var.full_name}',
                                                f'{contract.name}_{function.full_name}_{str(node_id)}',
                                                edge_type='use')
                else:
                    for node_id in state_var_use[state_var]:
                        contract_graph.add_edge(f'{function.contract_declarer.name}_{state_var.full_name}',
                                                f'{contract.name}_{function.full_name}_{str(node_id)}',
                                                edge_type='use')

        if sol_file_graph is None:
            sol_file_graph = deepcopy(contract_graph)
        elif sol_file_graph is not None:
            sol_file_graph = nx.compose(sol_file_graph, contract_graph)
    
    mapping = {node: i for i, node in enumerate(sol_file_graph.nodes)}
    sol_file_graph = nx.relabel_nodes(sol_file_graph, mapping)
    
    return sol_file_graph
       
'''获取节点全部信息'''
def get_node_info(node, list_sol_file_vul_info):

    node_type = str(node.type)

    if node.expression:
        node_expression = str(node.expression)
    else:
        if node.variable_declaration:
            node_expression = str(node.variable_declaration)
        else:
            node_expression = None

    node_token = "_".join([node_type, str(node_expression)])

    node_code_lines = node.source_mapping.lines

    node_vuln_info = None
    
    return node_type, node_expression, node_token, node_code_lines, node_vuln_info
