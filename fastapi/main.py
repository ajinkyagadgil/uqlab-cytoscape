from fastapi import FastAPI, Request
from typing import Optional
from datetime import date
import pandas as pd
from notears import linear, utils
import numpy as np
import json
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#############################################
# API: root call - welcome message
#############################################
@app.get("/")
async def root():
    return {"message": "Welcome to CAUSAL API!"}

#############################################
# FUNC: read the adjacency matrix from the json file
#############################################
def get_graph_from_json(data):
        
    # extract the nodes 
    no_nodes = len(data['nodes'])
    order_nodes = []
    for node in data['nodes']:
        #print(node['data']['id'], ': ', node['data']['name'])
        order_nodes.append(node['data']['id'])
        
    # initial mask
    mask = np.zeros((no_nodes, no_nodes))
    
    # extract the edges
    for edge in data['edges']:
        #print(edge['data']['id'], ': ', edge['data']['source'], ' -> ', edge['data']['target'])
        i = order_nodes.index(edge['data']['source'])
        j = order_nodes.index(edge['data']['target'])
        mask[i][j] = 1    
        
    return mask, order_nodes

#############################################
# API: get data from causal graph
#############################################
@app.post("/getData")
async def getData(graph_request: Request, no_samples: Optional[int] = None):
    
    graph_json = await graph_request.json()
    
    if no_samples == None:
        no_samples = 50
    
    # TODO: need to validate inputs as well as json to ensure its a DAG
    
    # get the causal graph 
    graph_adj, order_nodes = get_graph_from_json(graph_json)
    
    sem_type = 'gauss'
    X = utils.simulate_linear_sem(graph_adj, no_samples, sem_type)
    df = pd.DataFrame(X, columns=order_nodes)

    return df.to_json()

