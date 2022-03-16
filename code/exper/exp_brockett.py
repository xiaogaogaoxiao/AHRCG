import os
import csv
import autograd.numpy as np
from sklearn.datasets import make_spd_matrix

import pymanopt
from pymanopt.manifolds import Stiefel

from algorithms import ConjugateGradient, BetaTypes

from alg import ConjugateGradient1, BetaTypes1
from algsw import ConjugateGradient2, BetaTypes2

def create_cost(matrix):  #, dmatrix
    @pymanopt.function.Autograd
    def cost(X):
        return np.trace(X.T @ matrix @ X )#@ dmatrix

    return cost


if __name__ == "__main__":
    experiment_name = 'brockett'
    n_exp = 15

    if not os.path.isdir('res1'):
        os.makedirs('res1')
    path = os.path.join('res1', experiment_name + '.csv') #输出文件格式

    m = 20 #问题变量维数
    n = 5
    A = make_spd_matrix(m)  #生成A矩阵
    #N = np.diag([i for i in range(n)])

    cost = create_cost(A) #计算目标函数 , N
    manifold = Stiefel(m, n)  
    problem = pymanopt.Problem(manifold, cost, egrad=None) #包括流形的man，verbosity，obj,grad.


    for i in range(n_exp): # 每种问题平均计算10次
        res_list = []
        for beta_type in BetaTypes:  #四种beta类型
            solver = ConjugateGradient(beta_type=beta_type, maxiter=10000)
            res1 = solver.solve(problem)  
            res_list.append(res1[1])  #应该是输出第一个量函数值
            res_list.append(res1[2])  #输出第二个量迭代次数
        solver1 = ConjugateGradient1(BetaTypes1.Hybrid1, maxiter=10000)
        res1 = solver1.solve(problem)
        res_list.append(res1[1])
        res_list.append(res1[2])
        solver2 = ConjugateGradient1(BetaTypes1.Hybrid2, maxiter=10000)
        res1 = solver2.solve(problem)
        res_list.append(res1[1])
        res_list.append(res1[2])
        #res_list.append(res[3])
        solver3 = ConjugateGradient1(BetaTypes1.Hybrid3, maxiter=10000)
        res1 = solver3.solve(problem)
        res_list.append(res1[1])
        res_list.append(res1[2])
        
        
        with open(path, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(res_list)

