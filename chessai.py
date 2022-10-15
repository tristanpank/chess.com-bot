import chess
import chess.polyglot
from chess.polyglot import MemoryMappedReader
board = chess.Board()
#legal_moves = board.legal_moves
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

num_actions = 0

def player(board):
    if board.turn == False:
        return "b"
    elif board.turn == True:
        return "w"


# returns list of total moves as uci values
def actions(board):
    legal_moves = board.legal_moves
    total_actions = []
    total_actions = [mov for mov in legal_moves]
    # for move in board.legal_moves:
    #     total_actions.append(move)
    return total_actions

def result(board, action):
    new_board = board.copy()
    new_board.push(action)
    return new_board

def evaluation(board):
    # checks if game is over and returns massive score
    if board.is_checkmate():
        if board.turn:
            return -9999
        else:
            return 9999
    elif board.is_stalemate():
        return 0
    elif board.is_insufficient_material():
        return 0
    
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

    # if board.turn:
    #     return score
    # else:
    #     return -score

    return score

def minimax(board, depth):
    try:
        move = chess.polyglot.MemoryMappedReader(r"/Users/diego_only/repos/chess.com-bot/openings/human.bin").weighted_choice(board).move
        print(move)
        print(type(move))
        return move
    except:
        global num_actions
        num_actions = 0
        if depth == 0:
            return
        alpha = -10000
        beta = 10000
        best_value = -99999
        curr_player = player(board)
        total_actions = actions(board)
        action_values = []
        
        if board.turn:
            action_values = [(action, min_value(result(board, action), depth, alpha, beta)) for action in total_actions]
            # for action in total_actions:
            #     action_values.append((action, min_value(result(board, action), depth, alpha, beta)))
            print(action_values)
            curr_max = action_values[0]
            # curr_max = [action for action in action_values[1:] if action[-1] > curr_max[-1]]
            for action in action_values[1:]:
                if action[-1] > curr_max[-1]:
                    curr_max = action
            print()
            print(curr_max)
            print(f"Moves Searched: {num_actions}")
            return curr_max[0]

        else:
            action_values = [(action, max_value(result(board, action), depth, alpha, beta)) for action in total_actions]
            # for action in total_actions:
            #     action_values.append((action, max_value(result(board, action), depth, alpha, beta)))
            print(action_values)
            curr_min = action_values[0]
            # curr_min = [action for action in action_values[1:] if action[-1] < curr_min[-1]]
            for action in action_values[1:]:
                if action[-1] < curr_min[-1]:
                    curr_min = action
            print()
            print(curr_min)
            print(f"Moves Searched: {num_actions}")
            return curr_min[0]

def max_value(board, depth, alpha, beta, depth_set=False):
    global num_actions
    if depth == 0:
        score = evaluation(board)
        return evaluation(board)
    for action in actions(board):
        # print(action)
        num_actions += 1
        # if board.is_capture(action) and depth_set == False:
        #     depth = 2
        #     depth_set = True
        alpha = max(alpha, min_value(result(board, action), depth-1, alpha, beta, depth_set))
        # depth_set = False
        if beta <= alpha:
            return alpha
    return alpha

def min_value(board, depth, alpha, beta, depth_set=False):
    global num_actions
    if depth == 0:
        return evaluation(board)
    for action in actions(board):
    #     print(action)
        num_actions += 1
        # if board.is_capture(action) and depth_set == False:
        #     depth = 2
        #     depth_set = True
        beta = min(beta, max_value(result(board, action), depth-1, alpha, beta, depth_set))
        # depth_set = False
        if beta <= alpha:
            return beta
    return beta
   
    

