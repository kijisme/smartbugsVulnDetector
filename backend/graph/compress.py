import os
import argparse	
import networkx as nx


'''映射cfg和cg的相同函数节点'''
def mapping_cfg_and_cg_node_token(cfg, call_graph):
    
    # 存储函数节点的token映射
    dict_node_token_cfg_and_cg = {}

    # 遍历cfg的函数节点,添加token信息(type只有FUNCTION)
    for node, node_data in cfg.nodes(data=True):
        # 添加函数节点
        if node_data['node_type'] == 'FUNCTION':
            if node_data['node_token'] not in dict_node_token_cfg_and_cg:
                dict_node_token_cfg_and_cg[node_data['node_token']] = None
            dict_node_token_cfg_and_cg[node_data['node_token']] = {
                'cfg_node_id': node,
                'cfg_node_type': node_data['node_type']
            }
        # 添加状态变量节点
        if node_data['node_type'] == 'STATEVARIABLE':
            if node_data['node_token'] not in dict_node_token_cfg_and_cg:
                dict_node_token_cfg_and_cg[node_data['node_token']] = None
            dict_node_token_cfg_and_cg[node_data['node_token']] = {
                'cfg_node_id': node,
                'cfg_node_type': node_data['node_type']
            }

    # 遍历cg的函数节点,添加token信息(type有fallback_function\contract_function\state_variable)
    for node, node_data in call_graph.nodes(data=True):
        if node_data['node_token'] in dict_node_token_cfg_and_cg:
            dict_node_token_cfg_and_cg[node_data['node_token']]['call_graph_node_id'] = node
            dict_node_token_cfg_and_cg[node_data['node_token']]['call_graph_node_type'] = node_data['node_type'].upper()
        else:
            print(node_data['node_token'], ' is not existing.')
            # print(node_data['contract_name'])

    # 移走不在cg中的节点
    temp_dict = dict(dict_node_token_cfg_and_cg)
    for key, value in temp_dict.items():
        if 'call_graph_node_id' not in value or 'call_graph_node_type' not in value:
            dict_node_token_cfg_and_cg.pop(key, None)

    return dict_node_token_cfg_and_cg

'''根据cg对cfg添加call边'''
def add_new_cfg_edges_from_call_graph(cfg, dict_node_label, call_graph):
    
    list_new_edges_cfg = []
    for source, target, edge_data in call_graph.edges(data=True):
        source_cfg = None
        target_cfg = None
        edge_data_cfg = edge_data
        for value in dict_node_label.values():
            if value['call_graph_node_id'] == source:
                source_cfg = value['cfg_node_id']
            
            if value['call_graph_node_id'] == target:
                target_cfg = value['cfg_node_id']
        
        if source_cfg is not None and target_cfg is not None:
            list_new_edges_cfg.append((source_cfg, target_cfg, edge_data_cfg))
    
    cfg.add_edges_from(list_new_edges_cfg)

    return cfg
    
'''根据cg更新cfg函数节点类型'''
def update_cfg_node_types_by_call_graph_node_types(cfg, dict_node_label):
    for value in dict_node_label.values():
        cfg_node_id = value['cfg_node_id']
        # 将cfg中函数节点的类型转化为cg的节点类型
        cfg.nodes[cfg_node_id]['node_type'] = value['call_graph_node_type']


def generate_compress_graph(cfg, cg):
    
        # 映射图节点
        dict_node_token_cfg_and_cg = mapping_cfg_and_cg_node_token(cfg, cg)
        # 添加cfg函数调用边
        merged_graph = add_new_cfg_edges_from_call_graph(cfg, dict_node_token_cfg_and_cg, cg)
        # 更新节点类型
        update_cfg_node_types_by_call_graph_node_types(merged_graph, dict_node_token_cfg_and_cg)
        
        return merged_graph