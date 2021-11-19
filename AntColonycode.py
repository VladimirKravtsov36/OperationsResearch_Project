import numpy as np
from numpy import inf
import sys
import warnings
warnings.filterwarnings('ignore')

def read_matr(file):
    
    with open(file, 'r') as f:
        matr = [[int(num) for num in line.split(' ')] for line in f]
        
    return  matr 

#given values for the problems

d = read_matr(sys.argv[1])
d = np.array(d)

iteration = 200
n_ants = d.shape[0]
n_cities = d.shape[0]

# intialization part

m = n_ants
n = n_cities
e = 0.5         #evaporation rate
alpha = 2     #pheromone factor
beta = 1       #visibility factor

#calculating the visibility of the next city visibility(i,j)=1/d(i,j)

visibility = 1/d
visibility[visibility == inf] = 0

#intializing pheromone present at the paths to the cities

pheromone = 0.1*np.ones((m,n))

#intializing the rute of the ants with size rute(n_ants,n_cities+1) 
#note adding 1 because we want to come back to the source city

rute = np.ones((m,n+1))

for it in range(iteration):
    
    rute[:,0] = 1          #initial starting and ending positon of every ants '1' i.e city '1'
    
    for i in range(m):
        
        temp_visibility = np.array(visibility)         #creating a copy of visibility
        
        for j in range(n-1):
            
            combine_feature = np.zeros(5)     #intializing combine_feature array to zero
            cum_prob = np.zeros(5)            #intializing cummulative probability array to zeros
            
            cur_loc = int(rute[i,j]-1)        #current city of the ant
            
            temp_visibility[:,cur_loc] = 0     #making visibility of the current city as zero
            
            p_feature = np.power(pheromone[cur_loc,:],alpha)         #calculating pheromone feature 
            v_feature = np.power(temp_visibility[cur_loc,:],beta)  #calculating visibility feature
            
            p_feature = p_feature[:,np.newaxis]                     #adding axis to make a size[5,1]
            v_feature = v_feature[:,np.newaxis]                     #adding axis to make a size[5,1]
            
            combine_feature = np.multiply(p_feature,v_feature)     #calculating the combine feature
                        
            total = np.sum(combine_feature)                        #sum of all the feature
            
            probs = combine_feature/total   #finding probability of element probs(i) = comine_feature(i)/total
            
            cum_prob = np.cumsum(probs)     #calculating cummulative sum
            
            r = np.random.random_sample()   #randon no in [0,1)
            
            city = np.nonzero(cum_prob>r)[0][0]+1       #finding the next city having probability higher then random(r) 
            
            rute[i,j+1] = city              #adding city to route 
           
        left = list(set([i for i in range(1,n+1)])-set(rute[i,:-2]))[0]     #finding the last untraversed city to route
        
        rute[i,-2] = left                   #adding untraversed city to route
       
    rute_opt = np.array(rute)               #intializing optimal route
    
    dist_cost = np.zeros((m,1))             #intializing total_distance_of_tour with zero 
    
    for i in range(m):
        
        s = 0
        for j in range(n-1):
            
            s = s + d[int(rute_opt[i,j])-1,int(rute_opt[i,j+1])-1]   #calcualting total tour distance
        
        dist_cost[i]=s                      #storing distance of tour for 'i'th ant at location 'i' 
       
    dist_min_loc = np.argmin(dist_cost)             #finding location of minimum of dist_cost
    dist_min_cost = dist_cost[dist_min_loc]         #finging min of dist_cost
    
    best_route = rute[dist_min_loc,:]               #intializing current traversed as best route
    pheromone = (1-e)*pheromone                     #evaporation of pheromone with (1-e)
    
    for i in range(m):
        for j in range(n):
            dt = 1/dist_cost[i]
            pheromone[int(rute_opt[i,j])-1,int(rute_opt[i,j+1])-1] = pheromone[int(rute_opt[i,j])-1,int(rute_opt[i,j+1])-1] + dt   
            #updating the pheromone with delta_distance
            #delta_distance will be more with min_dist i.e adding more weight to that route  peromne

print(sys.argv[1])
print('Graph:')
print(d)
print()
print('best path:', best_route)
print('cost of the best path', int(dist_min_cost[0]) + d[int(best_route[-2])-1,0])
print()




