import hashiwokakero_classes as hc

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
    return islands


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
        else :
            drawing = "≈"
        if bridge.island1.x < bridge.island2.x:
            for i in range(bridge.island1.x + 1, bridge.island2.x * 2):
                islands[bridge.island1.y*2][i] = drawing
        else:
            for i in range(bridge.island2.x + 1, bridge.island1.x * 2):
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
    if (bridge.island1.x == bridge.island2.x) or (bridge.island1.y == bridge.island2.y):
        for i in range (bridge.island1.x, bridge.island2.x, 2):
            if islands[bridge.island1.y][i] != "≈":
                val = False
                break


    return val


#main
il = []
islands = loadIslands('islands.in', il)

bridges = []
printMap(islands)

finish = False

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
                    #TODO revisar valido en br encontrado con valor 0
                    if checkCoordinates(bri, br):
                        found = True
                        br.add_bridge()
                        drawBridges(br, islands)
                        printMap(islands)
                        break
                if not found:
                    bridges.append(bri)

                    drawBridges(bri, islands)
                    printMap(islands)
        else:
            print("Bridge")


    elif option == 2:
        print("Remove bridge")
    elif option == 3:
        finish = True
    else:
        print("Invalid option")
        