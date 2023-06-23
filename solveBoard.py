# coding=ISO8859-2
import numpy as np
from solver import Solver
import sys, getopt

global solutionMoves

def A_star(init_state, goal_state, max_iter, heuristic):
        solver = Solver(init_state, goal_state, heuristic, max_iter) 
        path = solver.solve_a_star() #Cria-se o objeto Solver (presente no arquivo solver.py) e realiza o solve via A*
        if len(path) == 0:
            print("Erro - N�o foi poss�vel solucionar")
            solutionMoves = []
            return solutionMoves
        #Se for poss�vel solucionar, printa no console e encerra o algoritmo de busca
        
        init_idx = init_state.flatten().tolist().index(0)
        init_i, init_j = init_idx // goal_state.shape[0], init_idx % goal_state.shape[0]
        
        print()
        print('ESTADO INICIAL')
        for i in range(goal_state.shape[0]):
            print(init_state[i, :]) 
        print()
        solutionMoves = []
        for node in reversed(path):
            #Printa no console a dire��o do movimento e o mhd total
            cur_idx = node.get_state().index(0)
            cur_i, cur_j = cur_idx // goal_state.shape[0], cur_idx % goal_state.shape[0]
            
            new_i, new_j = cur_i - init_i, cur_j - init_j
            if new_j == 0 and new_i == -1:
                print('Movendo para BAIXO  de ' + str((init_i, init_j)) + ' --> ' + str((cur_i, cur_j)))
                solutionMoves.append("down")
            elif new_j == 0 and new_i == 1:
                print('Movendo para CIMA  de ' + str((init_i, init_j)) + ' --> ' + str((cur_i, cur_j)))
                solutionMoves.append("up")
            elif new_i == 0 and new_j == 1:
                print('Movendo para ESQUERDA  de ' + str((init_i, init_j)) + ' --> ' + str((cur_i, cur_j)))
                solutionMoves.append("left")
            else:
                print('Movendo para DIREITA  de ' + str((init_i, init_j)) + ' --> ' + str((cur_i, cur_j)))
                solutionMoves.append("right")
            print('Score usando a heur�stica de manhatam � de ' + str(node.get_score() - node.get_level()) + ' no n�vel ' + str(node.get_level()))
        
            init_i, init_j = cur_i, cur_j
            
            #Printa no console a matriz ap�s o movimento
            for i in range(goal_state.shape[0]):
                print(np.array(node.get_state()).reshape(goal_state.shape[0], goal_state.shape[0])[i, :]) 
            print()
        print(solver.get_summary())
        return solutionMoves

    #Fun��o que chama a resolu��o via A* com os parametros de itera��o e heur�stica
    #Inicialmente adotou-se apenas a heur�stica de Manhattan, mas tamb�m poderia-se utilizar a heur�stica com base na qtd de blocos fora de posi��o
def solveBoardFun(initState, n):
    max_iter = 100000 #Valores acima de 100.000 podem causar overflow de mem�ria
    heuristic = "manhattan"
    algorithm = "a_star"
      
    init_state = initState
    
    goal_state = list(range(1, n*n))
    goal_state.append(0)

    init_state = np.array(init_state).reshape(n, n)
    goal_state = np.array(goal_state).reshape(n, n)
    
    solutionMoves = A_star(init_state, goal_state, max_iter, heuristic)
    return solutionMoves
