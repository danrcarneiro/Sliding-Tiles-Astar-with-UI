# coding=ISO8859-2
from queue import PriorityQueue, Queue
from game_state import GameState
import numpy as np
#!/usr/bin/python
import time

class Solver():
    def __init__(self, init_state, goal_state, heuristic_func = "manhattan", max_iter = 100000):
        self.__init_state = init_state
        self.__goal_state = goal_state
        self.__heuristic_func = heuristic_func
        self.__MAX = 100000
        self.__max_iter = max_iter
        self.__path = []
        self.__number_of_steps = 0
        self.__summary = ""
        
    def set_max_iter(self, max_iter):
        self.__max_iter = max_iter
        
    def get_path(self):
        return self.__path
    
    def get_summary(self):
        return self.__summary
        
    def solve_a_star(self):
        x_axis = [1, 0, -1,  0]
        y_axis = [0, 1,  0, -1]
        
        level = 0
        visited_nodes = set()
        
        start_time = time.process_time()
        
        nodes = PriorityQueue(self.__MAX)
        init_node = GameState(self.__init_state.flatten().tolist(), self.__goal_state.flatten().tolist(), level, parent = None, heuristic_func = self.__heuristic_func)
        nodes.put(init_node)
        
        epochs = 0
        while nodes.qsize() and epochs <= self.__max_iter:
            epochs += 1
            
            cur_node = nodes.get()
            cur_state = cur_node.get_state()
            print("Época: " + str(epochs) + ". Nós:" + str(cur_node.get_level()) + ". Tempo de execuçăo: " + str(np.round(time.process_time() - start_time, 4)) + "s", end="\r")
            #Se o nó já tiver sido visitado, ignora. Se năo tiver, adiciona aos nós visitados.
            if str(cur_state) in visited_nodes:
                continue
            visited_nodes.add(str(cur_state))
            
            # Checa se o estado atual é igual ao objetivo. Se for, finaliza
            if cur_state == self.__goal_state.flatten().tolist():
                self.__summary = str("O algoritmo A* levou " + str(cur_node.get_level()) + " passos para chegar a soluçăo, visitando um total " + str(epochs) + " estados e levando em torno de " + str(np.round(time.process_time() - start_time, 4)) + " segundos para chegar a soluçăo desejada.")
                while cur_node.get_parent():
                    self.__path.append(cur_node)
                    cur_node = cur_node.get_parent()
                break
            
            empty_tile = cur_state.index(0)
            i, j = empty_tile // self.__goal_state.shape[0], empty_tile % self.__goal_state.shape[0]
            
            cur_state = np.array(cur_state).reshape(self.__goal_state.shape[0], self.__goal_state.shape[0])
            for x, y in zip(x_axis, y_axis):
                new_state = np.array(cur_state)
                if i + x >= 0 and i + x < self.__goal_state.shape[0] and j + y >= 0 and j + y < self.__goal_state.shape[0]:
                    new_state[i, j], new_state[i+x, j+y] = new_state[i+x, j+y], new_state[i, j]
                    game_state = GameState(new_state.flatten().tolist(), self.__goal_state.flatten().tolist(), cur_node.get_level() + 1, cur_node, self.__heuristic_func)
                    if str(game_state.get_state()) not in visited_nodes:
                        nodes.put(game_state)
        # Informa se năo foi possível solucionar dentro o número limite de iteraçőes/estados explorados                
        if epochs > self.__max_iter:
            print('Esse tabuleiro năo é solucionável em menos de ' + str(self.__max_iter) + " iteraçőes")
        return self.__path