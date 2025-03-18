import 
import random
import math
import time
import copy
import matplotlib.pyplot as plt




def find_best_path(filename):
    
    data = tsplib95.load(filename)
    cities = list(data.get_nodes())


    def annealing(initial_state):
        
        initial_temp = 5000
    
        alpha = 0.99
        
        current_temp = initial_temp

        # Start by initializing the current state with the initial state
        solution = initial_state
        same_solution = 0
        same_cost_diff = 0
        
        while same_solution < 1500 and same_cost_diff < 15*len(cities):
            neighbor = get_neighbors(solution)
            
            # Check if neighbor is best so far
            cost_diff = get_cost(neighbor) - get_cost(solution)
            # if the new solution is better, accept it
            if cost_diff > 0:
                solution = neighbor
                same_solution = 0
                same_cost_diff = 0
                
            elif cost_diff == 0:
                solution = neighbor
                same_solution = 0
                same_cost_diff +=1
            # if the new solution is not better, accept it with a probability of e^(-cost/temp)
            else:
                if random.uniform(0, 1) <= math.exp(float(cost_diff) / float(current_temp)):
                    solution = neighbor
                    same_solution = 0
                    same_cost_diff = 0
                else:
                    same_solution +=1
                    same_cost_diff+=1
            # decrement the temperature
            current_temp = current_temp*alpha
            print(1/get_cost(solution), same_cost_diff)
        print(1/get_cost(solution))
        
        return solution, 1/get_cost(solution)

    def get_cost(state):
        distance = 0
        
        for i in range(len(state)):
            from_city = state[i]
            to_city = None
            if i+1 < len(state):
                to_city = state[i+1]
            else:
                to_city = state[0]
            distance += data.get_weight(from_city, to_city)
        fitness = 1/float(distance)
        return fitness
        
    def get_neighbors(state):
        
        neighbor = copy.deepcopy(state)
            
        
        func = random.choice([0,1,2,3])
        if func == 0:
            inverse(neighbor)
            
        elif func == 1:
            insert(neighbor)
            
        elif func == 2 :
            swap(neighbor)
        
        else:
            swap_routes(neighbor)
            
        return neighbor 

    def inverse(state):
    
        node_one = random.choice(state)
        new_list = list(filter(lambda city: city != node_one, state)) #route without the selected node one
        node_two = random.choice(new_list)
        state[min(node_one,node_two):max(node_one,node_two)] = state[min(node_one,node_two):max(node_one,node_two)][::-1]
        return state

    def insert(state):
        node_j = random.choice(state)
        state.remove(node_j)
        node_i = random.choice(state)
        index = state.index(node_i)
        state.insert(index, node_j)
        
        return state

    def swap(state):
        pos_one = random.choice(range(len(state)))
        pos_two = random.choice(range(len(state)))
        state[pos_one], state[pos_two] = state[pos_two], state[pos_one]
        
        return state

    def swap_routes(state):
        subroute_a = random.choice(range(len(state)))
        subroute_b = random.choice(range(len(state)))
        subroute = state[min(subroute_a,subroute_b):max(subroute_a, subroute_b)]
        del state[min(subroute_a,subroute_b):max(subroute_a, subroute_b)]
        insert_pos = random.choice(range(len(state)))
        for i in subroute:
            state.insert(insert_pos, i)
        return state

    best_route_distance = []
    best_route = []
    convergence_time = []
    start = time.time()
    route, route_distance = annealing(cities)
    time_elapsed = time.time() - start
    best_route_distance.append(route_distance)
    best_route.append(route)
    convergence_time.append(time_elapsed)
    
    return best_route,best_route_distance,convergence_time

