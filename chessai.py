import chess
import chess.polyglot
from chess import Board
import multiprocessing
board = Board()
num_cores = 1
pawntable = [
    0, 0, 0, 0, 0, 0, 0, 0,
    5, 10, 10, -20, -20, 10, 10, 5,
    5, -5, -10, 0, 0, -10, -5, 5,
    0, 0, 0, 20, 20, 0, 0, 0,
    5, 5, 10, 25, 25, 10, 5, 5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
    0, 0, 0, 0, 0, 0, 0, 0]

knightstable = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50]

bishopstable = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20]

rookstable = [
    0, 0, 0, 5, 5, 0, 0, 0,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    5, 10, 10, 10, 10, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0]

queenstable = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 5, 5, 5, 5, 5, 0, -10,
    0, 0, 5, 5, 5, 5, 0, -5,
    -5, 0, 5, 5, 5, 5, 0, -5,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20]

kingstable = [
    20, 30, 10, 0, 0, 10, 30, 20,
    20, 20, 0, 0, 0, 0, 20, 20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30]

cont = True
num_actions = 0
action_values = []
def player(board):
    if board.turn == False:
        return "b"
    elif board.turn == True:
        return "w"

def actions(board):
    total_actions = []
    for move in board.legal_moves:
        total_actions.append(move)
    return total_actions

def result(board, action):
    new_board = board.copy()
    new_board.push(action)
    return new_board

# checks if game is over and returns massive score
def evaluation(board:chess.Board):
    if board.is_stalemate():
        return -150
    elif board.is_insufficient_material():
        return -150
    elif board.is_repetition():
        return -150
    elif board.can_claim_fifty_moves():
        return -150
    elif board.is_checkmate():
        if board.turn:
            return -9999
        else:
            return 9999
    # calculates total number of each piece
    wp = len(board.pieces(chess.PAWN, chess.WHITE))
    bp = len(board.pieces(chess.PAWN, chess.BLACK))
    wn = len(board.pieces(chess.KNIGHT, chess.WHITE))
    bn = len(board.pieces(chess.KNIGHT, chess.BLACK))
    wb = len(board.pieces(chess.BISHOP, chess.WHITE))
    bb = len(board.pieces(chess.BISHOP, chess.BLACK))
    wr = len(board.pieces(chess.ROOK, chess.WHITE))
    br = len(board.pieces(chess.ROOK, chess.BLACK))
    wq = len(board.pieces(chess.QUEEN, chess.WHITE))
    bq = len(board.pieces(chess.QUEEN, chess.BLACK))
    # calculates score (for white)
    # based on num of pieces they have over black
    material = 100 * (wp - bp) + 320 * (wn - bn) + 330 * (wb - bb) + 500 * (wr - br) + 900 * (wq - bq)
    # mathces position of each piece type to position score table
    # positive score in favor for white
    pawnsq = sum([pawntable[i] for i in board.pieces(chess.PAWN, chess.WHITE)])
    pawnsq = pawnsq + sum([-pawntable[chess.square_mirror(i)]
        for i in board.pieces(chess.PAWN, chess.BLACK)])
    
    knightsq = sum([knightstable[i] for i in board.pieces(chess.KNIGHT, chess.WHITE)])
    knightsq = knightsq + sum([-knightstable[chess.square_mirror(i)] 
        for i in board.pieces(chess.KNIGHT, chess.BLACK)])
    
    bishopsq = sum([bishopstable[i] for i in board.pieces(chess.BISHOP, chess.WHITE)])
    bishopsq = bishopsq + sum([-bishopstable[chess.square_mirror(i)]
        for i in board.pieces(chess.BISHOP, chess.BLACK)])
    
    rooksq = sum([rookstable[i] for i in board.pieces(chess.ROOK, chess.WHITE)])
    rooksq = rooksq + sum([-rookstable[chess.square_mirror(i)]
        for i in board.pieces(chess.ROOK, chess.BLACK)])
    
    queensq = sum([queenstable[i] for i in board.pieces(chess.QUEEN, chess.WHITE)])
    queensq = queensq + sum([-queenstable[chess.square_mirror(i)]
        for i in board.pieces(chess.QUEEN, chess.BLACK)])

    kingsq = sum([kingstable[i] for i in board.pieces(chess.KING, chess.WHITE)])
    kingsq = kingsq + sum([-kingstable[chess.square_mirror(i)]
        for i in board.pieces(chess.KING, chess.BLACK)])
    # combines total_piece and positional scores
    score = material + pawnsq + knightsq + bishopsq + rooksq + queensq + kingsq
    return score

curr_board = 0
curr_depth = 0

def minimax(board, depth, cores):
    global cont
    global curr_board
    global curr_depth
    global num_cores
    num_cores = cores
    curr_board = board
    curr_depth = depth
    cont = True
    global num_actions
    try:
        move = chess.polyglot.MemoryMappedReader(r"./openings/human.bin").weighted_choice(board).move
        print(move)
        print(type(move))
        num_actions = 0
        return (move, 0)
    except:
        num_actions = 0
        if depth == 0:
            return
        alpha = -10000
        beta = 10000
        best_value = -99999
        curr_player = player(board)
        total_actions = [mov for mov in board.legal_moves]
        action_values = []
        num_of_actions = len(total_actions)
        action_values = core_choice(cores, num_of_actions, total_actions)
        if board.turn:
            print(action_values)
            curr_max = [-10000]
            alpha = -10000
            beta = 10000
            #set current_max to maximum scoring action, but check if it's a stalemate, and check if it allows the oppenent to force a stalemate, and evaluate based on that.
            for action in action_values:
                if action[-1] >= curr_max[-1]:
                    direct_eval = evaluation(result(curr_board, action[0]))
                    if direct_eval == -150 or direct_eval == -9999:
                        if direct_eval >= curr_max[-1]:
                            if direct_eval < 9000:
                                eval_2away = min_value(result(curr_board, action[0]), 1, alpha, beta)
                                number = None
                                for action2 in result(board,action[0]).legal_moves:
                                    if number != None:
                                        number2 = evaluation(result(result(curr_board, action[0]), action2[0]))
                                        if number2 == -150 or number2 == -9999 or number2 == 9999:
                                            if number2 < number:
                                                number = number2
                                if number == -150 or number == -9999 or number == 9999:
                                    if number >= curr_max[-1]:
                                        curr_max = (action[0], min(number2, direct_eval))
                                    else:
                                        print(f'Avoided Allowing Forced Draw by {eval_2away} because {number}!')
                                else:
                                    curr_max = (action[0], direct_eval)
                            else:
                                curr_max = (action[0], direct_eval)
                        else:
                            print(f'Avoided Stalemating by {action} because {direct_eval}!')
                    else:
                        eval_2away = min_value(result(curr_board, action[0]), 1, alpha, beta)
                        number = None
                        for action2 in result(board,action[0]).legal_moves:
                            if number == -150 or number == -9999:
                                number2 = evaluation(result(result(curr_board, action[0]), action2))
                                if number2 < number:
                                    number = number2
                            else:
                                number2 = evaluation(result(result(curr_board, action[0]), action2))
                                if number2 == -150 or number2 == -9999:
                                    number = number2
                        if number == -150 or number == -9999:
                            if number >= curr_max[-1]:
                                curr_max = (action[0], number)
                            else:
                                print(f'Avoided Allowing Forced Draw by {action} because {eval_2away}!')
                        else:
                            curr_max = action
            print()
            print(curr_max)
            return curr_max
        else:
            print(action_values)
            curr_min = [10000]
            alpha = -10000
            beta = 10000
            #set current_max to maximum scoring action, but check if it's a stalemate, and check if it allows the oppenent to force a stalemate, and evaluate based on that.
            for action in action_values:
                if action[-1] <= curr_min[-1]:
                    direct_eval = evaluation(result(curr_board, action[0]))
                    if direct_eval == -150 or direct_eval == -9999 or direct_eval == 9999:
                        if direct_eval <= curr_min[-1]:
                            if direct_eval < 9000:
                                eval_2away = max_value(result(curr_board, action[0]), 1, alpha, beta)
                                number = None
                                for action2 in result(board,action[0]).legal_moves:
                                    if number != None:
                                        number2 = evaluation(result(result(curr_board, action[0]), action2[0]))
                                        if number2 == -150 or number2 == -9999 or number2 == 9999:
                                            if number2 > number:
                                                number = number2
                                if number == -150 or number == -9999 or number == 9999:
                                    if number <= curr_min[-1]:
                                        curr_min = (action[0], min(number2, direct_eval))
                                    else:
                                        print(f'Avoided Allowing Forced Draw by {eval_2away} because {number}!')
                                else:
                                    curr_min = (action[0], direct_eval)
                            else:
                                curr_min = (action[0], direct_eval)
                        else:
                            print(f'Avoided Stalemating by {action} because {direct_eval}!')
                    else:
                        eval_2away = min_value(result(curr_board, action[0]), 1, alpha, beta)
                        number = None
                        for action2 in result(board,action[0]).legal_moves:
                            if number == -150 or number == -9999 or number == 9999:
                                number2 = evaluation(result(result(curr_board, action[0]), action2))
                                if number2 > number:
                                    number = number2
                            else:
                                number2 = evaluation(result(result(curr_board, action[0]), action2))
                                if number2 == -150 or number2 == -9999 or number2 == 9999:
                                    number = number2
                        if number == -150 or number == -9999 or number == 9999:
                            if number <= curr_min[-1]:
                                curr_min = (action[0], number)
                            else:
                                print(f'Avoided Allowing Forced Draw by {action} because {eval_2away}!')
                        else:
                            curr_min = action
            print()
            print(curr_min)
            return curr_min

def core_choice(cores, num_of_actions, total_actions):
    if cores == 4:
        actions1 = total_actions[:num_of_actions//4]
        actions1.append(board)
        actions2 = total_actions[num_of_actions//4:num_of_actions//2]
        actions2.append(board)
        actions3 = total_actions[num_of_actions//2:3*num_of_actions//4]
        actions3.append(board)
        actions4 = total_actions[3*num_of_actions//4:]
        actions4.append(board)
    elif cores == 8:
        actions1 = total_actions[:num_of_actions//8]
        actions1.append(board)
        actions2 = total_actions[num_of_actions//8:num_of_actions//4]
        actions2.append(board)
        actions3 = total_actions[num_of_actions//4:3*num_of_actions//8]
        actions3.append(board)
        actions4 = total_actions[3*num_of_actions//8:num_of_actions//2]
        actions4.append(board)
        actions5 = total_actions[num_of_actions//2:5*num_of_actions//8]
        actions5.append(board)
        actions6 = total_actions[5*num_of_actions//8:6*num_of_actions//8]
        actions6.append(board)
        actions7 = total_actions[6*num_of_actions//8:7*num_of_actions//8]
        actions7.append(board)
        actions8 = total_actions[7*num_of_actions//8:]
        actions8.append(board)
    q = multiprocessing.Queue()
    if cores == 4:
        actions1.append(q)
        actions2.append(q)
        actions3.append(q)
        actions4.append(q)
        actions1.append(curr_depth)
        actions2.append(curr_depth)
        actions3.append(curr_depth)
        actions4.append(curr_depth)
        p1 = multiprocessing.Process(target=perform_minimax, args=actions1)
        p2 = multiprocessing.Process(target=perform_minimax, args=actions2)
        p3 = multiprocessing.Process(target=perform_minimax, args=actions3)
        p4 = multiprocessing.Process(target=perform_minimax, args=actions4)
        p1.start()
        p2.start()
        p3.start()
        p4.start()
        p1.join()
        p2.join()
        p3.join()
        p4.join()
        p1.terminate()
        p2.terminate()
        p3.terminate()
        p4.terminate()
        action_values = q.get()
        action_values += q.get()
        action_values += q.get()
        action_values += q.get()
    elif cores == 8:
        actions1.append(q)
        actions2.append(q)
        actions3.append(q)
        actions4.append(q)
        actions5.append(q)
        actions6.append(q)
        actions7.append(q)
        actions8.append(q)
        actions1.append(curr_depth)
        actions2.append(curr_depth)
        actions3.append(curr_depth)
        actions4.append(curr_depth)
        actions5.append(curr_depth)
        actions6.append(curr_depth)
        actions7.append(curr_depth)
        actions8.append(curr_depth)
        p1 = multiprocessing.Process(target=perform_minimax, args=actions1)
        p2 = multiprocessing.Process(target=perform_minimax, args=actions2)
        p3 = multiprocessing.Process(target=perform_minimax, args=actions3)
        p4 = multiprocessing.Process(target=perform_minimax, args=actions4)
        p5 = multiprocessing.Process(target=perform_minimax, args=actions5)
        p6 = multiprocessing.Process(target=perform_minimax, args=actions6)
        p7 = multiprocessing.Process(target=perform_minimax, args=actions7)
        p8 = multiprocessing.Process(target=perform_minimax, args=actions8)
        p1.start()
        p2.start()
        p3.start()
        p4.start()
        p5.start()
        p6.start()
        p7.start()
        p8.start()
        p1.join()
        p2.join()
        p3.join()
        p4.join()
        p5.join()
        p6.join()
        p7.join()
        p8.join()
        p1.terminate()
        p2.terminate()
        p3.terminate()
        p4.terminate()
        p5.terminate()
        p6.terminate()
        p7.terminate()
        p8.terminate()
        action_values = q.get()
        action_values += q.get()
        action_values += q.get()
        action_values += q.get()
        action_values += q.get()
        action_values += q.get()
        action_values += q.get()
        action_values += q.get()
    return action_values

def perform_minimax(*actions):
    global num_actions
    action_list = [action for action in actions]
    curr_depth = action_list.pop()
    q = action_list.pop()
    board = action_list.pop()
    # print(actions)
    # print(action_list)
    alpha = -10000
    beta = 10000
    if board.turn:
        for action in action_list:
            curr_action = (action, min_value(result(board, action), curr_depth, alpha, beta))
            action_values.append(curr_action)
    else:
        for action in action_list:
            curr_action = (action, max_value(result(board, action), curr_depth, alpha, beta))
            action_values.append(curr_action)
    q.put(action_values)

def max_value(board, depth, alpha, beta,):
    global num_actions
    global cont
    if depth == 0:
        score = evaluation(board)
        if curr_depth >= 2:
            if score >= 9999:
                score2 = minimax(curr_board, curr_depth - 1, num_cores)[-1]
                if score2 >= 9999:
                    if curr_depth >= 3:
                        score3 = minimax(curr_board, curr_depth - 2, num_cores)[-1]
                        if score3 >= 9999:
                            if curr_depth >= 4:
                                score4 = minimax(curr_board, curr_depth - 3, num_cores)[-1]
                                if score4 >= 9999:
                                    return score + 3
                            else:
                                return score + 2
                        else:
                            return score + 1
                    return score + 1
                else:
                    return score
            else:
                return score
        else:
            return score
    one_less_deep = depth - 1
    for action in board.legal_moves:
        if one_less_deep == 0:
            if cont and (board.is_capture(action) or board.gives_check(action)):
                one_less_deep += 1
                cont = False
        alpha = max(alpha, min_value(result(board, action), one_less_deep, alpha, beta))
        if beta <= alpha:
            return alpha
    return alpha

def min_value(board, depth, alpha, beta):
    global num_actions
    global cont
    if depth == 0:
        score = evaluation(board)
        if curr_depth >= 2:
            if score >= 9999:
                score2 = minimax(curr_board, curr_depth - 1, num_cores)[-1]
                if score2 >= 9999:
                    if curr_depth >= 3:
                        score3 = minimax(curr_board, curr_depth - 2, num_cores)[-1]
                        if score3 >= 9999:
                            if curr_depth >= 4:
                                score4 = minimax(curr_board, curr_depth - 3, num_cores)[-1]
                                if score4 >= 9999:
                                    return score + 3
                            else:
                                return score + 2
                        else:
                            return score + 1
                    else:
                        return score + 1
                else:
                    return score
        return score
    one_less_deep = depth - 1
    for action in board.legal_moves:
        if one_less_deep == 0:
            if cont and (board.is_capture(action) or board.gives_check(action)):
                one_less_deep += 1
                cont = False
        beta = min(beta, max_value(result(board, action), one_less_deep, alpha, beta))
        if beta <= alpha:
            return beta
    return beta
   
    

