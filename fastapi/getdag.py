#!/usr/bin/env python3
from notears import linear, utils
import numpy as np
import argparse
import pandas as pd
import json

# read the adjacency matrix from the json file
def get_mask_from_json(filename_json):

    # read the json
    with open(filename_json) as f:
        data = json.load(f)
        
    # extract the nodes 
    no_nodes = len(data['nodes'])
    order_nodes = []
    for node in data['nodes']:
        #print(node['data']['id'], ': ', node['data']['name'])
        order_nodes.append(node['data']['id'])
        
    # initial mask
    mask = np.ones((no_nodes, no_nodes)) * np.nan
    
    # extract the edges
    for edge in data['edges']:
        #print(edge['data']['id'], ': ', edge['data']['source'], ' -> ', edge['data']['target'])
        i = order_nodes.index(edge['data']['source'])
        j = order_nodes.index(edge['data']['target'])
        mask[i][j] = 1    
        
    return mask, order_nodes
    
# save the new adjacency matrix to a json file
def save_json_from_mask(filename_result, df, W_notears):
    
    # get the nodes
    nodes = []
    for c in df.columns.to_list():
        tmp = {'data': {'id': c.replace(" ", "_"), 'name': c}}
        nodes.append(tmp)    
        
    # get the edges
    edges = []
    col = df.columns.to_list()
    ind = 0
    for i in range(len(col)):
        for j in range(len(col)):
            if (W_notears[i][j] != 0):
                tmp = {'data': {'id': 'edge'+str(ind), 
                                'source': col[i].replace(" ", "_"), 
                                'target': col[j].replace(" ", "_")}}
                edges.append(tmp)
                ind += 1
    
    # save new json
    data = {'nodes': nodes, 'edges': edges}
    with open(filename_result, 'w') as outfile:
        json.dump(data, outfile)

# the main function
def main(args):

    # get the arguments
    filename_csv = args.input_dataset_filename
    filename_json = args.input_mask_filename
    filename_result = args.output_mask_filename

    # get the mask
    mask, order_nodes = get_mask_from_json(filename_json)

    # get the training dataset
    df = pd.read_csv(filename_csv) 
    df = df[order_nodes]
    X_train = df.values

    # set additional parameters
    loss_type = 'logistic'
    lambda1 = 0.01

    # run constrained notears
    W_notears, res = linear.notears_linear(X_train, lambda1=lambda1, loss_type=loss_type, mask=mask, w_threshold=0.1)

    # save the new structure
    save_json_from_mask(filename_result, df, W_notears)

# arguments parser
def parse_args():
    parser = argparse.ArgumentParser(description='Run NOTEARS algorithm')
    parser.add_argument('input_dataset_filename', type=str, help='name csv file containing n by p data matrix')
    parser.add_argument('input_mask_filename', type=str, help='name json file containing the expert adjacency matrix')
    parser.add_argument('output_mask_filename', type=str, help='name json file to save the new adjacency matrix')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    main(args)

