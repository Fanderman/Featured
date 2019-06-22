import random
import math
import time
from copy import deepcopy
from treelib import Node, Tree

empty = (-1, -1)


def correct(x, y):
    return 0 <= x < 8 and 0 <= y < 8


def moves(board, player):
    options = set()

    for i in range(0, 8):
        for j in range(0, 8):

            if board[i][j] == player:
                for q in [-1, 0, 1]:
                    for w in [-1, 0, 1]:

                        if correct(i + q, j + w) and board[i + q][j + w] == -player:

                            multi = 2
                            while correct(i + multi * q, j + multi * w) and board[i + multi * q][j + multi * w] == -player:
                                multi += 1

                            if correct(i + multi * q, j + multi * w) and board[i + multi * q][j + multi * w] == 0:
                                options.add((i + multi * q, j + multi * w))

    return options


def random_player(board, player):
    options = moves(board, player)
    if len(options) == 0:
        return empty
    return random.choice(tuple(options))


def active_player(board, player):
    options = moves(board, player)
    if len(options) == 0:
        return empty
    a = input()
    b = input()
    if a == 'a':
        a = 0
    if a == 'b':
        a = 1
    if a == 'c':
        a = 2
    if a == 'd':
        a = 3
    if a == 'e':
        a = 4
    if a == 'f':
        a = 5
    if a == 'g':
        a = 6
    if a == 'h':
        a = 7
    mov = (int(b), int(a))
    return mov


def play(board, player, move):
    move_x = move[0]
    move_y = move[1]
    board[move_x][move_y] = player

    for q in [-1, 0, 1]:
        for w in [-1, 0, 1]:

            if correct(move_x + q, move_y + w) and board[move_x + q][move_y + w] == -player:

                multi = 2
                while correct(move_x + multi * q, move_y + multi * w) and board[move_x + multi * q][move_y + multi * w] == -player:
                    multi += 1

                if correct(move_x + multi * q, move_y + multi * w) and board[move_x + multi * q][move_y + multi * w] == player:
                    for m in range(1, multi):
                        board[move_x + m * q][move_y + m * w] = player

    return board


def simulation(board, player, passed):
    while passed < 2:
        move = random_player(board, player)

        if move[0] == -1:
            passed += 1

        else:
            passed = 0
            board = play(board, player, move)

        player = -player

    score = 0
    for i in range(8):
        for j in range(8):
            score += board[i][j]

    if score > 0:
        return 1
    if score < 0:
        return -1
    return 0


def mcts(board, player, c):
    global total
    global tree
    global board_dict
    start_total = total

    if (tuple(tuple(x) for x in board), player) not in board_dict:
        total += 1
        tree = Tree()
        tree.create_node(tag=total, identifier=total, data=[0, 0, deepcopy(board), player, 0, (4, 4)])
        board_dict[(tuple(tuple(x) for x in board), player)] = total
        local_root = total
    else:
        local_root = board_dict[(tuple(tuple(x) for x in board), player)]
    while total-start_total < 10000:
        #Selection
        x = tree.get_node(local_root)

        while not x.is_leaf():
            #print(x)
            mx = -1
            tot = x.data[1]
            children = x.fpointer

            for child in children:
                child = tree.get_node(child)
                #print(child)
                win = child.data[0]
                games = child.data[1]
                if child.data[3] == player:
                    win = games-win
                score = win/games + c*(math.sqrt(math.log(tot)/games))
                #print(score)
                if score > mx:
                    mx = score
                    x = child

                tot = x.data[1]

        #print(x)

        #Expansion
        current_board = x.data[2]
        current_player = x.data[3]
        options = moves(current_board, current_player)
        if len(options) > 0:
            base_board = deepcopy(current_board)
            for move in options:
                current_board = play(deepcopy(base_board), current_player, move)
                total += 1
                tree.create_node(tag=total, identifier=total, data=[0, 0, deepcopy(current_board), -current_player, 0, move], parent=x.identifier)
                board_dict[(tuple(tuple(x) for x in current_board), -current_player)] = total

                # Simulation
                result = simulation(current_board, -current_player, 0)

                # Propagation
                node = tree.get_node(total)
                end = False
                while not end:
                    if result == player:
                        node.data[0] += 1
                    node.data[1] += 1
                    if node.is_root():
                        end = True
                    else:
                        node = tree.get_node(node.bpointer)

        else:
            passes = x.data[4]

            total += 1
            if passes < 2:
                tree.create_node(tag=total, identifier=total, data=[0, 0, deepcopy(current_board), -current_player, passes+1, (-1, -1)], parent=x.identifier)
                board_dict[(tuple(tuple(x) for x in current_board), -current_player)] = total
                node = tree.get_node(total)
            else:
                node = x

            # Simulation
            result = simulation(current_board, -current_player, min(2, passes+1))

            # Propagation
            end = False
            while not end:
                if result == player:
                    node.data[0] += 1
                node.data[1] += 1
                if node.is_root():
                    end = True
                else:
                    node = tree.get_node(node.bpointer)

        #print(tree)
    x = tree.get_node(local_root)
    children = x.fpointer
    mx = -1
    answer = (-1, -1)
    for child in children:
        child = tree.get_node(child)
        #print(child)
        win = child.data[0]
        games = child.data[1]
        if win / games > mx:
            mx = win / games
            answer = child.data[5]
    #print(answer)

    return answer


def mcts_game(board, player, passed):
    while passed < 2:

        row = ' '
        for i in range(8):
            row += str(i)
        print(row)
        for i in range(8):
            row = ''
            row += str(i)
            for j in range(8):
                if table[i][j] == 1:
                    row += 'X'
                if table[i][j] == 0:
                    row += '-'
                if table[i][j] == -1:
                    row += 'O'
            print(row)

        if player == 1:
            #move = random_player(board, player)
            move = active_player(board, player)
            #move = mcts(board, player, math.sqrt(2))
        else:
            #move = random_player(board, player)
            #move = active_player(board, player)
            move = mcts(board, player, math.sqrt(2))
        print(move)
        if move[0] == -1:
            passed += 1
        else:
            passed = 0
            board = play(board, player, move)

        player = -player

    p1 = 0
    p2 = 0
    for i in range(0,8):
        for j in range(0,8):
            if board[i][j] == 1:
                p1 += 1
            if board[i][j] == -1:
                p2 += 1

    if p1 > p2:
        return 1
    if p1 < p2:
        return -1
    return 0


starting = -1
count = 0
for q in range(200):
    if q % 1 == 0:
        tree = Tree()
        total = -1
        board_dict = {}


        if starting == -1:
            #knowledge = open('base_first.txt', 'r').readlines()
            with open('base_first.txt', 'r') as knowledge:
                total = int(knowledge.readline())
                load_board = []
                next_line = knowledge.readline()
                while next_line != '':
                    line = next_line.split(' ')
                    load_row = []
                    #print(line)
                    if len(line) == 9:
                        for j in range(len(line) - 1):
                            load_row.append(int(line[j]))
                        load_board.append(load_row)
                    else:
                        ind = int(line[0])
                        wins = int(line[1])
                        games = int(line[2])
                        player = int(line[3])
                        parent = line[4]
                        passes = int(line[5])
                        move = (int(line[6]), int(line[7]))
                        if parent != 'None':
                            tree.create_node(tag=ind, identifier=ind,
                                             data=[wins, games, deepcopy(load_board), player, passes, move],
                                             parent=int(parent))
                        else:
                            tree.create_node(tag=ind, identifier=ind,
                                             data=[wins, games, deepcopy(load_board), player, passes, move])
                        board_dict[(tuple(tuple(x) for x in load_board), player)] = ind
                        load_board = []
                    next_line = knowledge.readline()
        else:
            #knowledge = open('base_second.txt', 'r').readlines()
            with open('base_second.txt', 'r') as knowledge:
                total = int(knowledge.readline())
                load_board = []
                next_line = knowledge.readline()
                while next_line != '':
                    line = next_line.split(' ')
                    load_row = []
                    #print(line)
                    if len(line) == 9:
                        for j in range(len(line) - 1):
                            load_row.append(int(line[j]))
                        load_board.append(load_row)
                    else:
                        ind = int(line[0])
                        wins = int(line[1])
                        games = int(line[2])
                        player = int(line[3])
                        parent = line[4]
                        passes = int(line[5])
                        move = (int(line[6]), int(line[7]))
                        if parent != 'None':
                            tree.create_node(tag=ind, identifier=ind,
                                             data=[wins, games, deepcopy(load_board), player, passes, move],
                                             parent=int(parent))
                        else:
                            tree.create_node(tag=ind, identifier=ind,
                                             data=[wins, games, deepcopy(load_board), player, passes, move])
                        board_dict[(tuple(tuple(x) for x in load_board), player)] = ind
                        load_board = []
                    next_line = knowledge.readline()

    table = []
    for i in range(8):
        table.append([])
        for j in range(8):
            table[i].append(0)

    table[3][3] = 1
    table[4][4] = 1
    table[3][4] = -1
    table[4][3] = -1

    result = mcts_game(table, starting, 0)
    if result == 1:
        count += 1
    print(result)
    print()
    for i in range(8):
        row = ''
        for j in range(8):
            if table[i][j] == 1:
                row += 'X'
            if table[i][j] == 0:
                row += '-'
            if table[i][j] == -1:
                row += 'O'
        print(row)
    print(count)

    """
    if q % 1 == 0:
        if starting == -1:
            #output = open('base_first.txt', 'w+')
            with open('base_first.txt', 'w+') as output:
                output.write(str(total) + '\n')
                for i in range(total):
                    res = tree.get_node(i)
                    if res is not None and tree.depth(res) <= 10:
                        node_board = res.data[2];
                        for line in node_board:
                            for nb in line:
                                output.write(str(nb) + ' ')
                            output.write('\n')
                        output.write(str(i) + ' ' + str(res.data[0]) + ' ' + str(res.data[1]) + ' ' + str(
                            res.data[3]) + ' ' + str(
                            res.bpointer) + ' ' + str(res.data[4]) + ' ' + str(res.data[5][0]) + ' ' + str(
                            res.data[5][1]) + ' ' + 'i' + ' ')
                        output.write('\n')
        else:
            #output = open('base_second.txt', 'w+')
            with open('base_second.txt', 'w+') as output:
                output.write(str(total) + '\n')
                for i in range(total):
                    res = tree.get_node(i)
                    if res is not None and tree.depth(res) <= 8:
                        node_board = res.data[2];
                        for line in node_board:
                            for nb in line:
                                output.write(str(nb) + ' ')
                            output.write('\n')
                        output.write(str(i) + ' ' + str(res.data[0]) + ' ' + str(res.data[1]) + ' ' + str(
                            res.data[3]) + ' ' + str(
                            res.bpointer) + ' ' + str(res.data[4]) + ' ' + str(res.data[5][0]) + ' ' + str(
                            res.data[5][1]) + ' ' + 'i' + ' ')
                        output.write('\n')
    """
