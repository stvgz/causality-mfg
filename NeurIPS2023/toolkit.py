import numpy as np
import os

def save_result(matrix, dataset=1, solution = 1, ):
    
    path_of_solution = f'./submission/solution{solution}'.format(solution)
    # create folder if not exist
    if not os.path.exists(path_of_solution):
        os.makedirs(path_of_solution)
    
    path = f'./submission/solution{solution}/{dataset}_graph_matrix.npy'.format(solution, dataset)
    
    graph_matrix = np.array(matrix)
    
    print("shape: ", graph_matrix.shape)
    
    np.save(path, graph_matrix)
    
    print(f'Saved solution {solution} for dataset {dataset} to {path}')
    
    
    
    
def check_shape():
    # check shape of the matrix for submission
    # N*N array for alarm types
    dataset_1 = 39
    dataset_2 = 49
    dataset_3 = 31
    dataset_4 = 30