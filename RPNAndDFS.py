import socket

hostname = "ctf10k.root-me.org"
port = 8002

# Solver for RPN formula
def RPN(data):
    res = 0
    text = data.split("\n")
    text2 = text[1].split(" ")
    i = 0

    #While our array contain more than 1 numbre, we continue to evaluate each expression
    while i < len(text2):
        if text2[i] == "+":
            text2[i-2] = str(int(text2[i-1]) + int(text2[i-2]))
            del text2[i]
            del text2[i-1]
            i = 0
        elif text2[i] == "-":
            text2[i-2] = str(int(text2[i-2]) - int(text2[i-1]))
            del text2[i]
            del text2[i-1]
            i = 0
        elif text2[i] == "x":
            text2[i-2] = str(int(text2[i-1]) * int(text2[i-2]))
            del text2[i]
            del text2[i-1]
            i = 0
        i += 1

    return text2[0]

# Same as last fonction with small change to adapt to the change of the format of bot messages
def RPNBis(data):
    res = 0
    text = data.split("\n")
    text2 = text[2].split(" ")
    i = 0

    while i < len(text2):
        if text2[i] == "+":
            text2[i-2] = str(int(text2[i-1]) + int(text2[i-2]))
            del text2[i]
            del text2[i-1]
            i = 0
        elif text2[i] == "-":
            text2[i-2] = str(int(text2[i-2]) - int(text2[i-1]))
            del text2[i]
            del text2[i-1]
            i = 0
        elif text2[i] == "x":
            text2[i-2] = str(int(text2[i-1]) * int(text2[i-2]))
            del text2[i]
            del text2[i-1]
            i = 0
        i += 1

    return text2[0]


def netcatRPN():
    # Connection to serveur
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("ctf10k.root-me.org", 8002))

    # We get the first question from the bot
    r = ""
    data = s.recv(4096)
    r += data.decode()

    res = RPN(r)
    res = res + "\n"
    s.sendall(res.encode())

    # We continue to recover every question the bot ask until it gave us the flag
    while 1:
        r = ""
        data = s.recv(512)
        r += data.decode()
        print(r)
        if r.find("flag") == -1:
            res = RPNBis(r)
            print(bytes(res,"ascii"))
            res = str(res) + "\n"
            s.sendall(res.encode())
        else:
            break

    s.close()

# Small function to check if x is in a list L
def is_in(n,l):
    for i in l:
        if n == i:
            return True
    return False

# Our main DFS function
def DFS(graph,n,node,end,res,stock):
    # Check of our counter
    if n == 0:
        return False

    # Check if A == B
    if node == end:
        return True

    # Our main recursion loop
    if n != 0:
        if is_in(end,graph[node]):
            return True
        else:
            for j in graph[node]:
                if not(is_in(j,stock)):
                    res = res or DFS(graph,n-1,j,end,res,stock + [node])
    return res

# Our parse function
def parser(msg):
    # Split the entry by "\n"
    text = msg.split("\n")
    graph = {}

    #For each line we get, we split it by " " then add the couple [Second word]:[all word after the eighth] that correspond to [node]:[neighbour]
    for i in text[2:len(text) - 1]:
        tmp = i.split(" ")
        if tmp[3] == "a":
            k = []
            for j in tmp[8:]:
                k.append(j.split(",")[0])
        else:
            k = []
        graph[tmp[1]] = k
    num = text[1].split(" ")

    # We call DFS then return the result
    return DFS(graph,int(len(text)),num[17],num[15],False,[])

# The main function for the DFS challenge
def netcatDFS():
    #Connection to server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("ctf10k.root-me.org", 8001))

    # For each question of the bot we answer it 
    while 1:
        r = ""
        data = s.recv(4096)
        r += data.decode()
        print(r)
        if r.find("flag") == -1:
            res = parser(r)
            if res:
                res = "yes" + "\n"
                print(res)
                s.sendall(res.encode())
            else:
                res = "no" + "\n"
                print(res)
                s.sendall(res.encode())
        else:
            break

    s.close()


netcatRPN()
netcatDFS()

