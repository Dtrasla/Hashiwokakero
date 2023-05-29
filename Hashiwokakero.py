import hashiwokakero_classes as hc
import heapq
import copy

def printMap(islands):
    marker = "   "
    for j in range(len(islands[0])):
        if j%2 == 0:
            marker += "[" + str(j//2) + "]"
        else:
            marker += " "
    print(marker)


    for i in range(len(islands)):
        if i%2 == 0:
            print(( "[" + str(i//2) + "]"), end=" ")
        else:
            print("   ", end=" ")
        for j in range(len(islands[i])):
            print(islands[i][j], end=" ")
        print()

def loadIslands(filename, il):
    with open(filename, 'r') as file:
        line = file.readline().strip()
        width, height = map(int, line.split(","))
        #Se duplican para dejar el espacio en la matriz para los puentes
        islands = [[0 for x in range(width*2)] for y in range(height*2)] 
        for i in range(height):
            line = file.readline().strip()
            for j in range(width):
                val = line[j]
                if val == "0":
                    islands[i*2][j*2] = "≈"
                else:
                    islands[i*2][j*2] = val
                    il.append(hc.Island(j, i, int(val)))
                islands[i*2][j*2+1] = "≈"
        for i in range(height):
            for j in range(width*2):
                islands[i*2+1][j] = "≈"
    addOptionsToIslands(il, islands)
    return islands

def addOptionsToIslands(il, islands):
    for i in range(len(il)):
        #Checks islands to the right
        found = False
        for j in range(il[i].x+1, len(islands[0])//2, 1):
            if islands[il[i].y*2][j*2] != "≈":
                #finds the island in the list
                for k in range(len(il)):
                    if il[k].x == j and il[k].y == il[i].y and not found:
                        il[i].options.append(il[k])
                        found = True
                        break
        #Checks islands to the left
        found = False
        for j in range(il[i].x-1, -1, -1):
            if islands[il[i].y*2][j*2] != "≈":
                #finds the island in the list
                for k in range(len(il)):
                    if il[k].x == j and il[k].y == il[i].y and not found:
                        il[i].options.append(il[k])
                        found = True
                        break
        #Checks islands above
        found = False
        for j in range(il[i].y-1, -1, -1):
            if islands[j*2][il[i].x*2] != "≈":
                #finds the island in the list
                for k in range(len(il)):
                    if il[k].x == il[i].x and il[k].y == j and not found:
                        il[i].options.append(il[k])
                        found = True
                        break
        #Checks islands below
        found = False
        for j in range(il[i].y+1, len(islands)//2, 1):
            if islands[j*2][il[i].x*2] != "≈":
                #finds the island in the list
                for k in range(len(il)):
                    if il[k].x == il[i].x and il[k].y == j and not found:
                        il[i].options.append(il[k])
                        found = True
                        break


def drawBridges(bridge, islands):
    drawing = ""
    if bridge.island1.x == bridge.island2.x:
        if bridge.num_bridges == 1:
            drawing = "|"
        elif bridge.num_bridges == 2:
            drawing = "║"
        else :
            drawing = "≈"
        if bridge.island1.y < bridge.island2.y:
            for i in range((bridge.island1.y*2)+1, bridge.island2.y*2):
                islands[i][bridge.island1.x*2] = drawing
        else:
            for i in range((bridge.island2.y*2)+1, bridge.island1.y*2):
                islands[i][bridge.island1.x*2] = drawing

    elif bridge.island1.y == bridge.island2.y:
        if bridge.num_bridges == 1:
            drawing = "-"
        elif bridge.num_bridges == 2:
            drawing = "="
        else:
            drawing = "≈"
        if bridge.island1.x < bridge.island2.x:
            for i in range(bridge.island1.x*2 + 1, bridge.island2.x * 2):
                islands[bridge.island1.y*2][i] = drawing
        else:
            for i in range(bridge.island2.x*2 + 1, bridge.island1.x * 2):
                islands[bridge.island1.y*2][i] = drawing
    

def checkCoordinates(bridge1, bridge2):
    if bridge1.island1.x == bridge2.island1.x and bridge1.island1.y == bridge2.island1.y:
        if bridge1.island2.x == bridge2.island2.x and bridge1.island2.y == bridge2.island2.y:
            return True

    elif bridge1.island1.x == bridge2.island2.x and bridge1.island1.y == bridge2.island2.y:
        if bridge1.island2.x == bridge2.island1.x and bridge1.island2.y == bridge2.island1.y:
            return True

    else:
        return False


def checkValidBridge(bridge, islands):
    val = True
    if (bridge.island1.x == bridge.island2.x): #or (bridge.island1.y == bridge.island2.y):
        if bridge.island1.y < bridge.island2.y:
            for i in range((bridge.island1.y*2)+1, bridge.island2.y*2):
                if islands[i][bridge.island1.x*2] != "≈":
                    val = False
        else:
            for i in range((bridge.island2.y*2)+1, bridge.island1.y*2):
                if islands[i][bridge.island1.x*2] != "≈":
                    val = False

    elif (bridge.island1.y == bridge.island2.y):
        if bridge.island1.x < bridge.island2.x:
            for i in range(bridge.island1.x*2 + 1, bridge.island2.x * 2):
                if islands[bridge.island1.y*2][i] != "≈":
                    val = False
        else:
            for i in range(bridge.island2.x*2 + 1, bridge.island1.x * 2):
                if islands[bridge.island1.y*2][i] != "≈":
                    val = False
    # if not val:
    #     print("Invalid bridge")
    return val



def is_solved(il):

    for i in range(len(il)):
        if il[i].num_bridges > 8:
            print("Invalid map")
            return False

    solved = True
    for i in range(len(il)):
        if il[i].sum != il[i].num_bridges:
            solved = False
    return solved


def solveSingleNeighborIslands(il, islands,bridges):
    for i in il:
        if len(i.options) == 1:
            newBridge = hc.Bridge(hc.Coordinate(i.x, i.y), hc.Coordinate(i.options[0].x, i.options[0].y))
            if checkValidBridge(newBridge, islands):
                i.addOne()
                i.options[0].addOne()
                bridges.append(newBridge)
                drawBridges(newBridge, islands)

            if i.num_bridges == 2:
                for br in bridges:
                    if checkCoordinates(newBridge, br) and br.num_bridges < 2 and i.sum <= i.num_bridges and i.options[0].sum <= i.options[0].num_bridges:
                        found = True
                        br.add_bridge()
                        drawBridges(br, islands)
                        i.addOne()
                        i.options[0].addOne()
    printMap(islands)

def auto_solver(il, bridges, islands, first=False):
    # if first:
    #     solveSingleNeighborIslands(il, islands, bridges)

    if is_solved(il):
        printMap(islands)
        print("Solved")
        return True

    pq = []
    for i in range(len(il)):
        if il[i].sum != il[i].num_bridges:
            pq.append(il[i])
    pq.sort(key=lambda x: x.num_bridges - x.sum, reverse=True)

    for i in range(len(pq)):

        if(pq[i].sum < pq[i].num_bridges):

            for j in range(len(pq[i].options)):

                if(pq[i].options[j].sum < pq[i].options[j].num_bridges):

                    newBridge = hc.Bridge(hc.Coordinate(pq[i].x, pq[i].y), hc.Coordinate(pq[i].options[j].x, pq[i].options[j].y))

                    found = False
                    for br in bridges:
                        if checkCoordinates(newBridge, br) and br.num_bridges < 2 and pq[i].sum <= pq[i].num_bridges and pq[i].options[j].sum <= pq[i].options[j].num_bridges:
                            found = True
                            br.add_bridge()
                            drawBridges(br, islands)
                            pq[i].addOne()
                            pq[i].options[j].addOne()
                            #print bridge to add
                            #print(newBridge.island1.x, newBridge.island1.y, newBridge.island2.x, newBridge.island2.y)
                            if auto_solver(il, bridges, islands):
                                return True
                            #printMap(islands)
                            break

                    if not found and checkValidBridge(newBridge, islands) and pq[i].sum <= pq[i].num_bridges and pq[i].options[j].sum <= pq[i].options[j].num_bridges:
                        bridges.append(newBridge)
                        drawBridges(newBridge, islands)
                        pq[i].addOne()
                        pq[i].options[j].addOne()
                        if auto_solver(il, bridges, islands):
                            return True
                        #print(newBridge.island1.x, newBridge.island1.y, newBridge.island2.x, newBridge.island2.y)
                        break


                    #Si no encuentra solucion, se regresa al estado anterior
                    found = False
                    for br in bridges:
                        if checkCoordinates(newBridge, br):
                            pq[i].subtractOne()
                            pq[i].options[j].subtractOne()
                            found = True
                            br.remove_bridge()
                            drawBridges(br, islands)
                            #print("Backtracking")
                            #bridges.remove(br)
                            #printMap(islands)
                            #break

    #print("No solution")
    return False


def test(il, bridges, islands, visited_options=None,first=False):
    if visited_options is None:
        visited_options = set()

    if is_solved(il):
        printMap(islands)
        print("Solved")
        return True

    pq = []
    for i in range(len(il)):
        if il[i].sum < il[i].num_bridges:
            pq.append(il[i])
    pq.sort(key=lambda x: x.num_bridges - x.sum, reverse=True)

    for i in range(len(pq)):
        if pq[i].sum < pq[i].num_bridges:
            for j in range(len(pq[i].options)):
                if pq[i].options[j].sum < pq[i].options[j].num_bridges:
                    newBridge = hc.Bridge(
                        hc.Coordinate(pq[i].x, pq[i].y),
                        hc.Coordinate(pq[i].options[j].x, pq[i].options[j].y)
                    )

                    found = False
                    for br in bridges:
                        if checkCoordinates(newBridge, br) and br.num_bridges < 2 and pq[i].sum <= pq[i].num_bridges and \
                                pq[i].options[j].sum <= pq[i].options[j].num_bridges:
                            found = True
                            br.add_bridge()
                            drawBridges(br, islands)
                            pq[i].addOne()
                            pq[i].options[j].addOne()
                            print(newBridge.island1.x, newBridge.island1.y, newBridge.island2.x, newBridge.island2.y)
                            #visited_options.add(newBridge)
                            if test(il, bridges, islands, visited_options):
                                return True
                            br.remove_bridge()
                            drawBridges(br, islands)
                            pq[i].subtractOne()
                            pq[i].options[j].subtractOne()
                            #visited_options.remove(newBridge)
                            printMap(islands)

                    if not found and checkValidBridge(newBridge, islands) and pq[i].sum <= pq[i].num_bridges and \
                            pq[i].options[j].sum <= pq[i].options[j].num_bridges:
                        bridges.append(newBridge)
                        drawBridges(newBridge, islands)
                        pq[i].addOne()
                        pq[i].options[j].addOne()
                        print(newBridge.island1.x, newBridge.island1.y, newBridge.island2.x, newBridge.island2.y)
                        #visited_options.add(newBridge)
                        if test(il, bridges, islands, visited_options):
                            return True
                        bridges.remove(newBridge)
                        drawBridges(newBridge, islands)
                        pq[i].subtractOne()
                        pq[i].options[j].subtractOne()
                        #visited_options.remove(newBridge)
                        printMap(islands)

    print("No solution")
    return False

    #TODO Iterar recursivamente cada isla en una cola hasta que no tenga mas jugadas posibles
    #TODO Si no se puede resolver, volver atras y probar otra jugada
    #TODO Si se llega a una solucion, imprimir y salir



#main
il = []
islands = loadIslands('islands.in', il)

bridges = []
printMap(islands)

finish = False

auto_solver(il, bridges, islands)
while not finish:
    print("1. Add bridge")
    print("2. Remove bridge")
    print("3. Exit")
    option = int(input("Select an option: "))
    if option == 1:
        print("Add bridge")
        x = int(input("x Island 1: "))
        y = int(input("y Island 1: "))

        if islands[y*2][x*2].isdigit():
            x1 = int(input("x Island 2: "))
            y1 = int(input("y Island 2: "))
            if islands[y1*2][x1*2].isdigit():
                bri = hc.Bridge(hc.Coordinate(x, y), hc.Coordinate(x1, y1))
                found = False
                for br in bridges:

                    if checkCoordinates(bri, br):
                        found = True
                        br.add_bridge()
                        drawBridges(br, islands)
                        printMap(islands)
                        break
                if not found and checkValidBridge(bri, islands):
                    bridges.append(bri)

                    #Changes sum in islands\
                    for i in range(len(il)):
                        if (il[i].x == bri.island1.x and il[i].y == bri.island1.y) or (il[i].x == bri.island2.x and il[i].y == bri.island2.y):
                            il[i].addOne()
                    drawBridges(bri, islands)
                    printMap(islands)

        else:
            print("Bridge")


    elif option == 2:
        x = int(input("x Island 1: "))
        y = int(input("y Island 1: "))
        if islands[y * 2][x * 2].isdigit():
            x1 = int(input("x Island 2: "))
            y1 = int(input("y Island 2: "))
            if islands[y1 * 2][x1 * 2].isdigit():
                bri = hc.Bridge(hc.Coordinate(x, y), hc.Coordinate(x1, y1))
                found = False
                for br in bridges:
                    if checkCoordinates(bri, br):
                        for i in range(len(il)):
                            if (il[i].x == bri.island1.x and il[i].y == bri.island1.y) or (
                                    il[i].x == bri.island2.x and il[i].y == bri.island2.y):
                                il[i].substractOne()
                        found = True
                        br.remove_bridge()
                        drawBridges(br, islands)
                        printMap(islands)
                        break
    elif option == 3:
        finish = True
    else:
        print("Invalid option")


#TODO Modificar estructura para poder crear grafo, problema de la reina arbol de decision con backtracking