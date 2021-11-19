import math
import sys
maxsize = float('inf')

def read_matr(file):
    
    with open(file, 'r') as f:
        matr = [[int(num) for num in line.split(' ')] for line in f]
        
    return  matr

'''Функция, копирующая временное решение в финальное решение'''
def copyToFinal(curr_path):
    final_path[:N + 1] = curr_path[:]
    final_path[N] = curr_path[0]

'''Функция, находящая ребро с минимальной стоимостью, входящее в вершину i'''
def firstMin(adj, i):
    min = maxsize
    for k in range(N):
        if adj[i][k] < min and i != k:
            min = adj[i][k]
    return min

'''Функция, находящая второе ребро с меньшей стоимостью, входящее в вершину i'''
def secondMin(adj, i):
    first, second = maxsize, maxsize
    for j in range(N):
        if i == j:
            continue
        if adj[i][j] <= first:
            second = first
            first = adj[i][j]

        elif (adj[i][j] <= second and
              adj[i][j] != first):
            second = adj[i][j]

    return second

'''Функция, которая принимает как аргументы:
curr_bound - нижнюю границу, 
curr_weight - текущую стоимость 
level - текущее положение во время движения по дереву, 
curr_path[] - там лежит текущее решение, которое позже будет перекопированно в final_path[]'''
def TSPRec(adj, curr_bound, curr_weight,
           level, curr_path, visited):
    global final_res

    '''Когда мы достигаем уровня N означает, что мы покрыли все вершины'''
    if level == N:

        '''Проверка того, что есть ребро из последней вершины до начальной'''
        if adj[curr_path[level - 1]][curr_path[0]] != 0:

            '''curr_res имеет длину такую же как у решения, которое мы получили'''
            curr_res = curr_weight + adj[curr_path[level - 1]] \
                [curr_path[0]]
            if curr_res < final_res:
                copyToFinal(curr_path)
                final_res = curr_res
        return

    ''' Для любого другого уровня итерации для всех вершин построить рекурсивное дерево поиска '''
    for i in range(N):
        '''Переходим в следующую вершину, если она не посещена и не 
та же самая, что и на предыдущем уровне'''
        if (adj[curr_path[level - 1]][i] != 0 and
                visited[i] == False):
            temp = curr_bound
            curr_weight += adj[curr_path[level - 1]][i]
            '''Разные вычисления curr_bound для второго уровня метода'''
            if level == 1:
                curr_bound -= ((firstMin(adj, curr_path[level - 1]) +
                                firstMin(adj, i)) / 2)
            else:
                curr_bound -= ((secondMin(adj, curr_path[level - 1]) +
                                firstMin(adj, i)) / 2)

            '''curr_bound + curr_weight это lower_bound для узла, в который мы прибыли.
            Если текущая нижняя граница меньше final_res,
             надо исследовать следующий узел'''
            if curr_bound + curr_weight < final_res:
                curr_path[level] = i
                visited[i] = True

                '''вызываем для следующего уровня'''
                TSPRec(adj, curr_bound, curr_weight,
                       level + 1, curr_path, visited)



            curr_weight -= adj[curr_path[level - 1]][i]
            curr_bound = temp

            # Перегружаем массив посещенных
            visited = [False] * len(visited)
            for j in range(level):
                if curr_path[j] != -1:
                    visited[curr_path[j]] = True


'''Функция, которая вычисляет конечный путь'''
def TSP(adj):
    ''' Вычисляет начальную нижнюю границу для начального узла
     Используем формулу 1/2 * (sum of first min + second min) для всех вершин
     Также инициализируем текущий маршрут и массив visited '''
    curr_bound = 0
    '''Текущая граница пока нулевая'''
    curr_path = [-1] * (N + 1)
    '''Пока у нас нет маршрута'''
    visited = [False] * N
    '''Пока ничего не посетили'''

    ''' Вычисляем начальную текущую границу границу как сумму первого и второго кратчайшего ребра'''
    for i in range(N):
        curr_bound += (firstMin(adj, i) + secondMin(adj, i))

    '''Округляем текущую границу до целого числа'''
    curr_bound = math.ceil(curr_bound / 2)

    '''Начинаем в нулевой вершине'''
    visited[0] = True
    curr_path[0] = 0

    '''Вызываем функцию TSRPec для для первого шага и нулевой вершины'''
    TSPRec(adj, curr_bound, 0, 1, curr_path, visited)



adj = read_matr(sys.argv[1])
N = len(adj)

'''Конечный маршрут из N+1 точек'''
final_path = [None] * (N + 1)

'''Отслеживает уже посещенные вершины'''
visited = [False] * N

'''Cохраняет финальную минимальную стоимость кратчайшего тура '''
final_res = maxsize

'''Вызываем функцию'''
TSP(adj)

print(sys.argv[1])
for row in adj:
    print(row)
print()
print("Minimum cost :", final_res)
print("Path Taken : ", end=' ')
for i in range(N + 1):
    print(final_path[i], end=' ')
print()
