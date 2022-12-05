
#Implementacion de algoritmo CKY para analisis sintactico

#Yolanda Elizondo Chapa - A01137848
#Daniel Salvador Cázares García  - A01197517
#Angel Corrales Sotelo - A01562052
#Izael Manuel Rascón Durán - A01562240
#Yoceline Aralí Mata Ledezma - A01562116


T = ["time", "flies", "like", "an", "arrow"]
N = ["S", "NP", "VP", "PP", "Det", "Nominal", "Verb", "Preposition", "Noun"]


#Reglas
R = {
    "S": [["NP", "VP", 0.8]],
    "NP": [["Det", "Nominal", 0.3], ["Nominal", "Nominal", 0.2], ["time", 0.002], ["flies", 0.002], ["arrow", 0.002]],
    "Nominal": [["Nominal", "Noun", 0.1], ["Nominal", "PP", 0.2], ["time", 0.002], ["flies", 0.002], ["arrow", 0.002]], 
    "VP": [["Verb", "NP", 0.3], ["Verb", "PP", 0.2], ["time", 0.004], ["flies", 0.008], ["like", 0.008]],
    "PP": [["Preposition", "NP", 0.1]],
    "Verb": [["time", 0.01],  ["flies", 0.02], ["like", 0.02]],
    "Noun": [["time", 0.01],  ["flies", 0.01], ["arrow", 0.01]],
    "Det": [["an", 0.05]],
    "Preposition": [["like", 0.05]] 
}


#Función que imprime el árbol con el que se llegó a una variable
def imprimirCamino(tablaCky, camino, n, s):
    print("S", s, " (4,4)", "probabilidad:", tablaCky[0][n-1]["S"][s])
    
    recorrerCamino(camino, tablaCky, camino[0][n-1]["S"][0], "")
    

def recorrerCamino(camino, tablaCky, curNode, espacio):
    izq = curNode[0]
    der = curNode[1]

    print(espacio, izq[-1],"(", izq[0], ",", izq[1], ") Probabilidad:", tablaCky[izq[0]][izq[1]][izq[-1]], "Palabra:", T[izq[1]],  end="")
    
    if izq[0] != izq[1]:
        print("->")
        recorrerCamino(camino, tablaCky, camino[izq[0]][izq[1]][izq[2]][0], espacio+"   ")
    
    print()
    print(espacio, der[-1],"(", der[0], ",", der[1], ") Probabilidad:", tablaCky[der[0]][der[1]][der[-1]], "Palabra:", T[der[1]], end="")
    if der[0] != der[1]: 
        print("->")
        recorrerCamino(camino, tablaCky, camino[der[0]][der[1]][der[2]][0], espacio+"   ")
        
    return


#Algoritmo de CKY
def cky(w):
    n = len(w)
     
    #Inicializar tablas con el tamaño de la oración recibida
    tablaCky = [[dict([]) for j in range(n)] for i in range(n)]
    camino = [[dict([]) for j in range(n)] for i in range(n)]
   
    for j in range(0, n):
 
        #Recorrer reglas
        for llave, reglas in R.items():
            for regla in reglas:
               
               #Revisar si es terminal
                if len(regla) == 2 and regla[0] == w[j]:
                    prob = regla[-1] 

                    if not tablaCky[j][j].get(llave):
                        tablaCky[j][j][llave] = []

                    #Añadir probabilidad para la variable
                    tablaCky[j][j][llave].append(prob)
                             

        for i in range(j, -1, -1):  
              
            for k in range(i, j + 1):    
                
                #Recorrer reglas
                for llave, reglas in R.items():
                    for regla in reglas:
                       
                        if (k + 1 < n): 
                            #Revisar si es terminal
                            if len(regla) == 3 and regla[0] in tablaCky[i][k] and regla[1] in tablaCky[k+1][j]:
                                prob = regla[-1] * tablaCky[i][k][regla[0]][0] * tablaCky[k+1][j][regla[1]][0]

                                if not tablaCky[i][j].get(llave):
                                    tablaCky[i][j][llave] = []
                                    camino[i][j][llave] = []

                                #Añadir probabilidad calculada para la variable
                                tablaCky[i][j][llave].append(prob)
                                #Añadir celdas que llevaron a ese resultado a la matriz de camino
                                camino[i][j][llave].append([[i,k, regla[0]],[k+1, j, regla[1]]])

 
    #Elegir S con mayor probabilidad  
    mayorProbabilidad = -1
    probabilidadesS = tablaCky[0][n-1]["S"]

    for i in range(len(probabilidadesS)):
        if(probabilidadesS[i] > mayorProbabilidad):
            mayorProbabilidad = probabilidadesS[i]
            s = i
    
    #Llamar a función de imprimirCamino para mostrar como se llegó a la S con mayor probabilidad
    print("Arbol de S con mayor probabilidad")
    imprimirCamino(tablaCky, camino, n, s)


#Llamar al algoritmo
cky(T)

