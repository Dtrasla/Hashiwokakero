def printMap(islands):
    for i in range(len(islands)):
        for j in range(len(islands[i])):
            print(islands[i][j], end=" ")
        print()

def loadIslands(filename):
    with open(filename, 'r') as file:
        line = file.readline().strip()
        width, height = map(int, line.split(","))
        #Se duplican para dejar el espacio en la matriz para los puentes
        islands = [[0 for x in range(width*2)] for y in range(height*2)] 
        for i in range(height):
            line = file.readline().strip()
            for j in range(width):                    
                islands[i*2][j*2] = int(line[j])
                islands[i*2][j*2+1] = "~"
        for i in range(height):
            for j in range(width*2):
                islands[i*2+1][j] = "~"
    return islands


#main
islands = loadIslands('islas.in')
printMap(islands)