from bs4 import BeautifulSoup
import time
import re
import os
import sys
import urllib3


bridges = []


class Node:
    def __init__(self, xpos, ypos, val, name):
        self.x = xpos
        self.y = ypos
        self.v = val
        self.n = name
        self.p = val

class Bridge:
    def __init__(self, node1Name , node2Name):
        self.n1 = node1Name
        self.n2 = node2Name


#Returns True if the two nodes are connected
def isBridge(name1 , name2) :
    global bridges
    for b in bridges :
        if (b.n1 == name1 and b.n2 == name2) or (b.n1 == name2 and b.n2 == name1) :
            return True
    return False

def isNodeAt(posx , posy , nodes) :
    for n in nodes :
        if n.x == posx and n.y == posy :
            return True
    return False

def getDoubleBridgeAt(posx , posy , nodes) :
    global bridges
    count = 0
    for b in bridges :
       val1 = b.n1
       val2 = b.n2
       for n in nodes :
           if n.n == val1 :
               node1 = n
           elif n.n == val2 :
               node2 = n


       if node1.x == node2.x :
           if posx == node1.x :
               if (posy < node2.y and posy > node1.y) or (posy > node2.y and posy < node1.y) :
                   if count == 1 :
                        return b
                   else :
                        count = count + 1
       if node1.y == node2.y :
           if posy == node1.y :
               if (posx < node2.x and posx > node1.x) or (posx > node2.x and posx < node1.x) :
                   if count == 1 :
                        return b
                   else :
                        count = count + 1
    return False

def isDoubleBridgeAt(posx , posy , nodes) :
    global bridges
    count = 0
    for b in bridges :
       val1 = b.n1
       val2 = b.n2
       for n in nodes :
           if n.n == val1 :
               node1 = n
           elif n.n == val2 :
               node2 = n


       if node1.x == node2.x :
           if posx == node1.x :
               if (posy < node2.y and posy > node1.y) or (posy > node2.y and posy < node1.y) :
                   if count == 1 :
                        return True
                   else :
                        count = count + 1
       if node1.y == node2.y :
           if posy == node1.y :
               if (posx < node2.x and posx > node1.x) or (posx > node2.x and posx < node1.x) :
                   if count == 1 :
                        return True
                   else :
                        count = count + 1
    return False

def isDoubleBridge(name1 , name2) :
    global bridges
    count = 0
    for b in bridges :
        if (b.n1 == name1 and b.n2 == name2) or (b.n1 == name2 and b.n2 == name1) :
            if count == 1 :
                return True
            else :
                count = count + 1
    return False


#Creates a bridge between 2 nodes.
#It is assumed that this bridge can be created.
def formBridge(node1 , node2) :
    global bridges
    node1.v = node1.v - 1
    node2.v = node2.v - 1
    bridges.append(Bridge(node1.n , node2.n))

def printUnsolvedBoard(filePath) :
    print("Unsolved : ")
    print()
    f = open(filePath , "r")
    lines = f.readlines()
    for l in lines :
        lineString = ""
        for c in l :
            if c == 'x' or c == '\n' :
                lineString = lineString + " "
            else :
                lineString = lineString + c
        print(lineString)

def isHorizontalDoubleBridgeAt(x , y , nodes) :
    global bridges
    for n in nodes :
        if x == n.x and y == n.y :
            return False
    if isDoubleBridgeAt(x , y , nodes) == False :
        return False

    b = getDoubleBridgeAt(x , y , nodes)
    n1 = getNode(b.n1 , nodes)
    n2 = getNode(b.n2 , nodes)
    if n1.y == n2.y :
        return True
    return False



def isHorizontalBridgeAt(x , y , nodes) :
    global bridges
    for n in nodes :
        if x == n.x and y == n.y :
            return False
    if isBridgeAt(x , y , nodes) == False :
        return False

    b = getBridgeAt(x , y , nodes)
    n1 = getNode(b.n1 , nodes)
    n2 = getNode(b.n2 , nodes)
    if n1.y == n2.y :
        return True
    return False
    
    
def getBridgeAt(posx , posy , nodes) :
    global bridges
    for b in bridges :
       val1 = b.n1
       val2 = b.n2
       for n in nodes :
           if n.n == val1 :
               node1 = n
           elif n.n == val2 :
               node2 = n

       if node1.x == node2.x :
           if posx == node1.x :
               if (posy < node2.y and posy > node1.y) or (posy > node2.y and posy < node1.y) :
                   return b
       if node1.y == node2.y :
           if posy == node1.y :
               if (posx < node2.x and posx > node1.x) or (posx > node2.x and posx < node1.x) :
                   return b
    return False

#Returns True if there is a bridge at the given point.
def isBridgeAt(posx , posy , nodes) :
    global bridges
    for b in bridges :
       val1 = b.n1
       val2 = b.n2
       for n in nodes :
           if n.n == val1 :
               node1 = n
           elif n.n == val2 :
               node2 = n

       if node1.x == node2.x :
           if posx == node1.x :
               if (posy < node2.y and posy > node1.y) or (posy > node2.y and posy < node1.y) :
                   return True
       if node1.y == node2.y :
           if posy == node1.y :
               if (posx < node2.x and posx > node1.x) or (posx > node2.x and posx < node1.x) :
                   return True
    return False


def printBoard(filePath , nodes) :
    print("Solved : ")
    print()
    f = open(filePath , "r")
    solution = ""
    lines = f.readlines()
    y = 1
    x = 1
    for l in lines :
        lineString = "    "
        x = 1
        for c in l :
            if isHorizontalDoubleBridgeAt(x , y , nodes) :
                lineString = lineString + "═"
                solution = solution + "="
            elif isDoubleBridgeAt(x , y , nodes) :
                lineString = lineString + "║"
                solution = solution + "n"
            elif isHorizontalBridgeAt(x , y , nodes) :
                lineString = lineString + "─"
                solution = solution + "-"
            elif isBridgeAt(x , y , nodes) :
                lineString = lineString + "│"
                solution = solution + "i"
            elif c != 'x' and c != '\n':
                lineString = lineString + c
                solution = solution + "x"
            elif c!= '\n':
                lineString = lineString + " "
                solution = solution + "x"
            else :
                lineString = lineString + " "

                        
            x = x + 1
        print(lineString)
        y = y + 1
    print(solution)
    return solution

#Reads the board from the given file and
#returns the proper node array
def readIntoData(filePath) :
    names = []
    for i in range(5000) :
        names.append(i)
    f = open(filePath , "r")
    lines = f.readlines()
    y = 1
    x = 1
    nodes = []
    count = 0
    for l in lines :
        x = 1
        for c in l :
            if c == 'x' or c == '\n' :
                pass;
            else :
                val = eval(c)
                nodes.append(Node(x , y , val , names[count]))
                count = count + 1
            x = x + 1
        y = y + 1
    return nodes


def solveTrivialNode(node , nodes) :
    if node.v == 0 :
        return 0
    global bridges
    validNeighbors = getNeighbors(node , nodes)
    numberNeighbors = numNeighbors(node , nodes)
    total = 0
    for n in validNeighbors :
        if n != '' :
            total = total + getNodeVal(n , nodes)
            
    if numberNeighbors != 0 :
        if node.v/numberNeighbors == 2 :
            for n in validNeighbors :
                if n != '' :
                    print("Solving trivial node {}...".format(node.n))
                    neighbor = getNode(n, nodes)
                    formBridge(node , neighbor)
                    formBridge(node , neighbor)
                    solveTrivialNode(neighbor , nodes)
                    return 1
        elif node.v == 1 and numberNeighbors == 1 :
            for n in validNeighbors :
                if n != '' :
                    print("Solving trivial node {}...".format(node.n))
                    neighbor = getNode(n , nodes)
                    formBridge(node , neighbor)
                    solveTrivialNode(neighbor , nodes)
                    return 1
        elif node.v == total :
            for n in validNeighbors :
                if n != '':
                    if getNodeVal(n , nodes) == 2 and getNodeVal(node.n , nodes) >= 2:
                        print("Solving trivial node {}...".format(node.n))
                        neighbor = getNode(n , nodes)
                        formBridge(node , neighbor)
                        formBridge(node , neighbor)
                        solveTrivialNode(neighbor , nodes)
                        return 1
                    else :
                        print("Solving trivial node {}...".format(node.n))
                        neighbor = getNode(n , nodes)
                        formBridge(node , getNode(n , nodes))
                        solveTrivialNode(neighbor , nodes)
                        return 1
#        elif node.v == numNeighborBridges(node , nodes) :
#            for n in validNeighbors :
#                if n != '' :
#                    if getNodeVal(n , nodes) >= 2 and getNodeVal(node.n , nodes) >= 2:
#                        print("Solving trivial node {}...".format(node.n))
#                        neighbor = getNode(n , nodes)
#                        formBridge(node , neighbor)
#                        formBridge(node , neighbor)
#                        solveTrivialNode(neighbor , nodes)
#                        return 1
#                    else :
#                        print("Solving trivial node {}...".format(node.n))
#                        neighbor = getNode(n , nodes)
#                        formBridge(node , neighbor)
#                        solveTrivialNode(neighbor , nodes)
#                        return 1

    return 0 


def numNeighborBridges(node , nodes) :
    validNeighbors = getNeighbors(node , nodes)
    total = 0
    for n in validNeighbors :
        if n != '' :
            if getNodeVal(n , nodes) > 1 :
                total = total + 2
            elif getNodeVal(n , nodes) == 1 :
                total = total + 1
    return total

def fancySolve(node , nodes) :         
    if node.v == 0 :
        return 0
    global bridges
    validNeighbors = getNeighbors(node , nodes)
    numberNeighbors = numNeighbors(node , nodes)
    for n in validNeighbors :
        if n != '' :
            neighbor = getNode(n , nodes)
            neighborNumber = numNeighbors(neighbor , nodes)
            if neighborNumber == 2 and neighbor.v >= 3 and node.v >= 1:
                print("Solving fancy node {}...".format(node.n))
                formBridge(node , neighbor)
                return 1
            elif neighborNumber == 3 and neighbor.v >= 5 and node.v >= 1 :
                print("Solving fancy node {}...".format(node.n))
                formBridge(node , neighbor)
                return 1
            elif neighborNumber == 4 and neighbor.v >= 7 and node.v >= 1:
                print("Solving fancy node {}...".format(node.n))
                formBridge(node , neighbor)
                return 1
    return 0

def getNodeVal(name , nodes) :
    return getNode(name , nodes).v

def solveBoard(nodes) :
    count = 1
    while count >= 1 :
        count = 0
        for n in nodes :
            count = count + solveTrivialNode(n , nodes)
        if count == 0 :
            for n in nodes :
                count = count + fancySolve(n , nodes)
                if count > 0 :
                    break

def getNode(name , nodes) :
    for n in nodes :
        if n.n == name :
            return n

def numNeighbors(node , nodes) :
    nodeList = getNeighbors(node , nodes)
    count = 0
    for i in nodeList :
        if i != '' :
            count = count + 1
    return count







#Returns a list of all the neighboring nodes
def getNeighbors(node , nodes) :
    closest = 99
    #Format : [Down , Up , Left , Right]
    neighbors = ['' , '' , '' , '']
    counter = 0
    found = ''
    for n in nodes :
        if node.x == n.x and (node.y - n.y != 0) and (abs(node.y - n.y) < closest) and (n.y > node.y):
            do = 1
            for y in range(abs(node.y - n.y)) :
                if y != 0 :
                    if isBridgeAt(node.x , node.y + y , nodes) or isNodeAt(node.x , node.y + y , nodes):
                        do = 0
            if do == 1 :
                if isBridge(node.n , n.n) == False :
                    if n.v > 0 :
                        if n.p != 1 or node.p != 1 :
                            found = n.n
            closest = abs(node.y - n.y)
    if closest != 99 :
        neighbors[counter] = found
    counter = counter + 1

    closest = 99
    found = ''
    for n in nodes :
        if node.x == n.x and (node.y - n.y != 0) and (abs(node.y - n.y) < closest) and (n.y < node.y):
            do = 1
            for y in range(abs(node.y - n.y)) :
                if y != 0 :
                    if isBridgeAt(node.x , n.y + y , nodes) or isNodeAt(node.x , n.y + y , nodes) :
                        do = 0
            if do == 1 :
                if isBridge(node.n , n.n) == False :
                    if n.v > 0 :
                        if n.p != 1 or node.p != 1 :
                            found = n.n
            closest = abs(node.y - n.y)
    if closest != 99 :
        neighbors[counter] = found
    counter = counter + 1

    closest = 99
    found = ''
    for n in nodes :
        if node.y == n.y and (node.x - n.x != 0) and (abs(node.x - n.x) < closest) and (n.x < node.x):
            do = 1
            for x in range(abs(node.x - n.x)) :
                if x != 0 :
                    if isBridgeAt(n.x + x, node.y, nodes) or isNodeAt(n.x + x , node.y , nodes) :
                        do = 0
            if do == 1 :
                if isBridge(node.n , n.n) == False :
                    if n.v > 0 :
                        if n.p != 1 or node.p != 1 :
                            found = n.n
            closest = abs(node.x - n.x)
    if closest != 99 :
        neighbors[counter] = found
    counter = counter + 1

    closest = 99
    found = ''
    for n in nodes :
        if node.y == n.y and (node.x - n.x != 0) and (abs(node.x - n.x) < closest) and (n.x > node.x):
            do = 1
            for x in range(abs(node.x - n.x)) :
                if x != 0 :
                    if isBridgeAt(node.x + x, node.y, nodes) or isNodeAt(node.x + x , node.y , nodes) :
                        do = 0
            if do == 1 :
                if isBridge(node.n , n.n) == False :
                    if n.v > 0 :
                        if n.p != 1 or node.p != 1 :
                            found = n.n
            closest = abs(node.x - n.x)
    if closest != 99 :
        neighbors[counter] = found
    counter = counter + 1

    return neighbors



xPos = []
yPos = []

#Get the HTML code
http = urllib3.PoolManager()
response = http.request('GET' , 'www.puzzle-bridges.com/?size=11')

page_source = response.data

#Make it readable
soup = BeautifulSoup(page_source , 'html.parser')
for line in soup.get_text().split("\n") :
    if line.startswith("25x25") :
        ID = line[-9:].replace(',' , '')
        print("ID : {}".format(ID))
    elif line.find("wall[") != -1 :
        print(line)
        matches = re.findall(r"\[(\w+)\]" , line)
        if len(matches) == 2 :
            print(matches[0])
            print(matches[1])
            try :
                xPos.append(eval(matches[1]))
                yPos.append(eval(matches[0]))
            except :
                pass

param = soup.find("input" , {"name":"param"})
ansV = soup.find("input" , {"name":"ansV"})

try :
    os.remove("Image.png")
    os.remove("board.data")
except OSError :
    pass

os.system("curl \"www.puzzle-bridges.com/task.php?id=" + ID + "\&size=11\" > Image.png")
os.system("tesseract -psm 6 --tessdata-dir . Image.png output -l mylang")
os.system("python3 removeExcess.py")
time.sleep(0.1)

nodesFile = open("nodes.txt" , "r")
nodeLines = nodesFile.readlines()
nodes = []
for l in nodeLines :
    for c in l :
        if c != '\n' :
            nodes.append(c)

f = open("board.data" , "w")
count = 0
for y in range(25) :
    for x in range(25) :
        if xPos[count] == x and yPos[count] == y :
            try : 
                print(nodes[count])
                f.write(nodes[count])
                count = count + 1
            except :
                pass
        else :
            f.write('x')
    f.write('\n')
f.close()

startTime = time.time()
filePath = "board.data"
nodes = readIntoData(filePath)
for n in nodes :
    print("Neighbors of node {} : ".format(n.n))
    print(getNeighbors(n , nodes))
    print("Number : {}".format(numNeighbors(n , nodes)))

solveBoard(nodes)

for b in bridges :
    print("Bridge : {} to {}".format(b.n1 , b.n2))

print()
printUnsolvedBoard(filePath)
print()
solution = printBoard(filePath , nodes)

endTime = time.time()

print("Total time : {}".format(endTime - startTime))
