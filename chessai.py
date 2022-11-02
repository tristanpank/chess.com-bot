
import chess
import chess.polyglot
from chess import Board, square_mirror
import multiprocessing
board = Board()
num_cores = 1
pawntable = (
    0, 0, 0, 0, 0, 0, 0, 0,
    5, 10, 10, -20, -20, 10, 10, 5,
    5, -5, -10, 0, 0, -10, -5, 5,
    0, 0, 0, 20, 20, 0, 0, 0,
    5, 5, 10, 25, 25, 10, 5, 5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
    0, 0, 0, 0, 0, 0, 0, 0)

knightstable = (
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50)

bishopstable = (
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20)

rookstable = (
    0, 0, 0, 5, 5, 0, 0, 0,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    5, 10, 10, 10, 10, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0)

queenstable =(
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 5, 5, 5, 5, 5, 0, -10,
    0, 0, 5, 5, 5, 5, 0, -5,
    -5, 0, 5, 5, 5, 5, 0, -5,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20)

kingstable = (
    20, 30, 10, 0, 0, 10, 30, 20,
    20, 20, 0, 0, 0, 0, 20, 20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30)

cont = True
num_actions = 0
action_values = []

def player(board: chess.Board):
    if board.turn == False:
        return "b"
    elif board.turn == True:
        return "w"

def actions(board):
    return [move for move in board.legal_moves]

def result(board, action):
    new_board = board.copy()
    new_board.push(action)
    return new_board

# checks if game is over and returns massive score
def evaluation(board:chess.Board):
    if board.is_stalemate() or board.is_insufficient_material() or board.is_repetition() or board.can_claim_fifty_moves():
        if board.turn:
            stalemate_value = -150
        else:
            stalemate_value = 150
        return stalemate_value
    elif board.is_checkmate():
        if board.turn:
            return -9999
        else:
            return 9999
    # calculates total number of each piece
    wp, bp, wn, bn, wb, bb, wr, br, wq, bq = board.pieces(chess.PAWN, chess.WHITE), board.pieces(chess.PAWN, chess.BLACK), board.pieces(chess.KNIGHT, chess.WHITE), board.pieces(chess.KNIGHT, chess.BLACK), board.pieces(chess.BISHOP, chess.WHITE), board.pieces(chess.BISHOP, chess.BLACK), board.pieces(chess.ROOK, chess.WHITE), board.pieces(chess.ROOK, chess.BLACK), board.pieces(chess.QUEEN, chess.WHITE), board.pieces(chess.QUEEN, chess.BLACK)
    # calculates score (for white)
    # based on num of pieces they have over black
    # mathces position of each piece type to position score table
    # positive score in favor for white
    pawnsq, knightsq, bishopsq, rooksq, queensq, kingsq = sum([pawntable[i] for i in wp]) - sum([pawntable[square_mirror(i)] for i in bp]), sum([knightstable[i] for i in wn]) - sum([knightstable[square_mirror(i)] for i in bn]), sum([bishopstable[i] for i in wb]) - sum([bishopstable[square_mirror(i)] for i in bb]), sum([rookstable[i] for i in wr]) - sum([rookstable[square_mirror(i)] for i in br]), sum([queenstable[i] for i in wq]) - sum([queenstable[square_mirror(i)] for i in bq]), sum([kingstable[i] for i in board.pieces(chess.KING, chess.WHITE)]) - sum([kingstable[square_mirror(i)] for i in board.pieces(chess.KING, chess.BLACK)])
    # combines total_piece and positional scores
    wp, bp, wn, bn, wb, bb, wr, br, wq, bq = len(wp), len(bp), len(wn), len(bn), len(wb), len(bb), len(wr), len(br), len(wq), len(bq)
    material = 100 * (wp - bp) + 320 * (wn - bn) + 330 * (wb - bb) + 500 * (wr - br) + 900 * (wq - bq)
    score = material + pawnsq + knightsq + bishopsq + rooksq + queensq + kingsq
    return score

curr_board = 0
curr_depth = 0

def minimax(board, depth, cores):
    global cont
    global curr_board
    global curr_depth
    global num_cores
    global stalemate_value
    curr_board, curr_depth, num_cores, cont = board, depth, cores, 1
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
            stalemate_value = -150
            print(action_values)
            curr_max = [-10000]
            alpha = -10000
            beta = 10000
            #set current_max to maximum scoring action, but check if it's a stalemate, and check if it allows the oppenent to force a stalemate, and evaluate based on that.
            for action in action_values:
                if action[-1] >= curr_max[-1]:
                    direct_eval = evaluation(result(curr_board, action[0]))
                    if direct_eval == -150 or direct_eval == -9999 or direct_eval == 9999:
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
                                curr_max = (action[0], direct_eval + 5)
                        else:
                            print(f'Avoided Stalemating by {action} because {direct_eval}!')
                    else:
                        eval_2away = min_value(result(curr_board, action[0]), 1, alpha, beta)
                        number = None
                        if eval_2away > 9000:
                            curr_max = (action[0], eval_2away + 4)
                        else:
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
            stalemate_value = 150
            print(action_values)
            curr_min = [10000]
            alpha = -10000
            beta = 10000
            #set current_max to maximum scoring action, but check if it's a stalemate, and check if it allows the oppenent to force a stalemate, and evaluate based on that.
            for action in action_values:
                if action[-1] <= curr_min[-1]:
                    direct_eval = evaluation(result(curr_board, action[0]))
                    if direct_eval == -150 or direct_eval == 9999:
                        if direct_eval <= curr_min[-1]:
                            if direct_eval < 9000:
                                eval_2away = max_value(result(curr_board, action[0]), 1, alpha, beta)
                                number = None
                                for action2 in result(board,action[0]).legal_moves:
                                    if number != None:
                                        number2 = evaluation(result(result(curr_board, action[0]), action2[0]))
                                        if number2 == -150 or number2 == 9999:
                                            if number2 > number:
                                                number = number2
                                if number == -150 or number == 9999:
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
                            if number == -150 or number == 9999:
                                number2 = evaluation(result(result(curr_board, action[0]), action2))
                                if number2 > number:
                                    number = number2
                            else:
                                number2 = evaluation(result(result(curr_board, action[0]), action2))
                                if number2 == -150 or number2 == 9999:
                                    number = number2
                        if number == -150 or number == 9999:
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
        actions1.append(cont)
        actions2.append(cont)
        actions3.append(cont)
        actions4.append(cont)
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
        actions1.append(cont)
        actions2.append(cont)
        actions3.append(cont)
        actions4.append(cont)
        actions5.append(cont)
        actions6.append(cont)
        actions7.append(cont)
        actions8.append(cont)
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
    action_list = [action for action in actions]
    conts = action_list.pop()
    curr_depth = action_list.pop()
    q = action_list.pop()
    board = action_list.pop()
    # print(actions)
    # print(action_list)
    alpha = -10000
    beta = 10000
    if board.turn:
        action_values = [(action, min_value(result(board, action), curr_depth, alpha, beta, conts)) for action in action_list]
    else:
        action_values = [(action, max_value(result(board, action), curr_depth, alpha, beta, conts)) for action in action_list]
    q.put(action_values)

def max_value(board, depth, alpha, beta, conts = 2):
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
    temp = conts
    for action in board.legal_moves:
        if one_less_deep == 0 and temp <= 1:
            if board.is_capture(action) or board.gives_check(action):
                one_less_deep += 1
                conts += 1
                #print(action, conts)
            # else:
            #     res = result(board,action)
            #     for square in res.attacks(action.to_square):
            #         if res.piece_type_at(square) != None and  res.piece_type_at(square) > 1:
            #             one_less_deep += 1
            #             conts += 1
            #             break
        alpha = max(alpha, min_value(result(board, action), one_less_deep, alpha, beta, conts))
        if beta <= alpha:
            return alpha
    return alpha

def min_value(board, depth, alpha, beta, conts = 2):
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
    temp = conts
    for action in board.legal_moves:
        if one_less_deep == 0 and temp <= 1:
            if board.is_capture(action) or board.gives_check(action):
                one_less_deep += 1
                conts += 1
                #print(action, conts)
            # else:
            #     res = result(board,action)
            #     for square in res.attacks(action.to_square):
            #         if res.piece_type_at(square) != None and res.piece_type_at(square) > 1:
            #             one_less_deep += 1
            #             conts += 1
            #             break
        beta = min(beta, max_value(result(board, action), one_less_deep, alpha, beta, conts))
        if beta <= alpha:
            return beta
    return beta
   
    

