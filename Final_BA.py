import time
import random
import matplotlib.pyplot as plt
import numpy as np
#kB = 1
#%matplotlib notebook

class Node: # klasa Węzeł, jaka jest każdy widzi
    index = 0
    spin = 0
    energy = 0
    connections = []
    def __init__(self, index, connections):
        self.index = index
        self.connections = connections


#rsv - random spin value do generowani spinów
def rsv():
    x = random.uniform(0, 1)
    if x<0.5:
        return (-1)
    else:
        return 1


def creat_BA_graph(iterations,m,m0, J):#podaję liczbę stworoznych nowych węzłów, liczbę tworoznych połąćzeń, startową liczbę wezłów
    #tworze listę węzłów i początkowe połączenia
    nodes_list = []
    for i in range(m0): 
        index=i
        connections = []
        for x in range(m0):
            if (x) != index: 
                connections.append(x)
            else: pass
        node = Node(index, connections)
        node.connections.sort()
        node.spin = 1
        nodes_list.append(node)
    # dodaję kolejne weżły zgodnie z algorytmeme twoerzania BA    
    for i in range(iterations-m0):
        new_connections_list = random.sample(range(m0+i),m) 
        connections = []
        index=m0+i
        for x in range(m):
            connections.append(new_connections_list[x])
            nodes_list[new_connections_list[x]].connections.append(index)#doje "inofrmację zwrotną" do węzłą do któego stowrziny węzeł został przydzielony
        node = Node(index, connections)
        node.spin = 1
        node.connections.sort()
        nodes_list.append(node)
    #liczę energię każdego węzła   
    for items in nodes_list:
        items.energy = 0
        for spins in items.connections:
            one_energy = -J*items.spin*nodes_list[spins].spin
            items.energy = items.energy+one_energy
            
    return nodes_list #zrwaca listę węzłów, dzięki temu nie ma potrzeby globalnej listy węzłów




def show(nodes_list):#pokazuje indeks węzłą oraz z jakimi węzłąmi jest połączony
     for items in nodes_list:
        print(" ")
        print(items.index)
        #print(items.spin)
        print(items.energy)
        print(len(items.connections))


            

def energy_sim_3(graph, T,J,break_value, kB_val):
    #to są elemnty do obrazowania:
    magn_list = []
    energy_list = []
    iteration_list = []
    break_sum = 0
    nodes_list = graph
    while(True):
        beta = 1/(kB_val*T)
        node = random.choice(nodes_list)
        index = node.index
        #obliczanie starej energii całkowiete
        old_total_energy = 0
        for items in nodes_list:
            old_total_energy += items.energy
            #zmiana spinu w losowo wybranym węźle i liczenie energi węzłów
        nodes_list[index].spin = -1*nodes_list[index].spin
        for items in nodes_list:
            items.energy = 0
            for spins in items.connections:
                one_energy = -J*items.spin*nodes_list[spins].spin
                items.energy = items.energy+one_energy
        #obliczanie energii całkowitej po zmainie spinu        
        new_total_energy = 0
        for items in nodes_list:
            new_total_energy += items.energy
    
        delta_E = new_total_energy - old_total_energy
        if(delta_E<0):
            pass
        elif(delta_E>=0):
            probability = np.exp(-beta*delta_E)
            rand = random.uniform(0,1)
            if(rand<=probability):
                pass
            elif(rand>probability):
                nodes_list[index].spin = -1*nodes_list[index].spin
                for items in nodes_list:
                    items.energy = 0
                    for spins in items.connections:
                        one_energy = -J*items.spin*nodes_list[spins].spin
                        items.energy = items.energy+one_energy
    
        magnetyzacja = 0 
        magn = 0
        for items in graph:
            magn += items.spin
        magnetyzacja = magn/len(nodes_list)
        magn_list.append(magnetyzacja)
        energy_list.append(old_total_energy)
        #print("{}   {}".format(break_sum, magnetyzacja))
        iteration_list.append(sum)
        break_sum +=1
        if (magnetyzacja <= 0.05 or break_sum > break_value): #break_sum>break_value or 
            break
            #else:
                
        else:
            pass 
    
    return magn_list[-1]


node_number_list = [100, 200, 500, 1000, 2000, 5000, 10000]
#GŁÓWNA PĘTLA

for number in node_number_list:

    it_list = []
    mag_list = []
    temp_list = []
    error_list = []
    start = time.time()

    ''' ZMIENIAJ NAZWE PLIKU ZA KAZDYM RAZEM'''
    dane = open(r"C:\Users\Public\Studia\Semestr_6\Laby_Spec\Final\dane_{}.txt".format(number), "w+")
    n_wezlow = number
    stala_kB = 1
    itera = 2.5*number
    J = 1
    graph = creat_BA_graph(n_wezlow,5,10,J)#węzły łacznie, l połączeń, startowe węzły, J
    print(r"start dla {}".format(number))
    n=1
    if(number <= 200):
        n = 20
    elif(number <= 2000):
        n = 5
    else:
        n=3
            
        
    for i in range(10):
        print(i)
        mag_out = 0
        suma = 0
        tymczas_magn = []
        for j in range(n):
            #T = (((i+1)))*10
            T = 40+ (((i+1))/2)
            mag_out = energy_sim_3(graph, T, J, itera, stala_kB) #graf, tem, J, iteracje, kB
            suma+=mag_out
            tymczas_magn.append(mag_out)
            for node in graph:
                node.spin = 1
                
        
        suma_kwad = 0
        for i in tymczas_magn:
            suma_kwad+=(i-(suma/n))**2
            
        #error_list.append(np.sqrt((1/(n*(n-1)))*suma_kwad))   
        mag_list.append(suma/n)
        temp_list.append(T)
        
        
        dane.write(str(T))
        dane.write("     ")
        dane.write(str(suma/n))
        dane.write("     ")
        #dane.write(str(np.sqrt(np.sqrt((1/(n*(n-1)))*suma_kwad))))
        dane.write("\n")   
    dane.close()


    print("")    
    end = time.time()
    print(end - start)
    print("")   
 
    plt.scatter(temp_list, mag_list)
    plt.title(r"Magne od T, {} wezlow".format(n_wezlow))
    plt.xlabel("T[K]")
    plt.ylabel("Magnetyzacja")
    #plt.errorbar(0,error_list)
    plt.show()
    










