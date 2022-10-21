
driver = ""
def main():
    import chess
    import time
    import math
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import multiprocessing
    from chessai import player, actions, result, evaluation, minimax, max_value, min_value, perform_minimax, board
    global is_capture
    global en_passant
    global driver
    global moves2
    s = Service("./chromedriver/chromedriver")

    driver = webdriver.Chrome(service = s)

    driver.get("https://www.chess.com/login")
    search = driver.find_element(By.XPATH, value='//*[@id="username"]')
    search.send_keys('Dekshunari2')

    search = driver.find_element(By.ID, value='password')
    search.send_keys('Chessrobot1')
    search = driver.find_element(By.ID, value = 'login')
    search.click()

    '''
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, 'Play a Friend'))
    )
    search = driver.find_element(By.LINK_TEXT, value = 'Play a Friend')
    search.click()
    search = driver.find_element(By.CLASS_NAME, value = 'play-friend-search-input-input')
    search.send_keys('Dekshunari')
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, 'dekshunari'))
    )
    search = driver.find_element(By.LINK_TEXT, value = 'dekshunari')
    search.click()

    #Change time of game, dunno but needed to wait 10
    driver.implicitly_wait(10)
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="board-layout-sidebar"]/div/div[2]/div/div[4]/div/div[2]/button'))
    )
    search = driver.find_element(By.XPATH, '//*[@id="board-layout-sidebar"]/div/div[2]/div/div[4]/div/div[2]/button')
    search.click()
    #click 30 min
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="board-layout-sidebar"]/div/div[2]/div/div[4]/div/div[2]/div/div[3]/div[2]/button[1]'))
    )
    search = driver.find_element(By.XPATH, value = '//*[@id="board-layout-sidebar"]/div/div[2]/div/div[4]/div/div[2]/div/div[3]/div[2]/button[1]')
    search.click()

    #click white pieces
    search = driver.find_element(By.XPATH, value = '//*[@id="board-layout-sidebar"]/div/div[2]/div/div[4]/div/div[3]/div[1]/button[1]')
    search.click()
    #Switch to unrated
    search = driver.find_element(By.XPATH, value = '//*[@id="board-layout-sidebar"]/div/div[2]/div/div[4]/div/div[3]/div[2]/div')
    search.click()
    #Play
    search = driver.find_element(By.XPATH, value = '//*[@id="board-layout-sidebar"]/div/div[2]/div/div[4]/div/button')
    search.click()
    '''
    driver.implicitly_wait(20)
    move_num = 0
    last_move = 0
    playing_robot = input('Playing robot?')
    cores = int(input('Number of cores? '))
    deep = int(input('Depth: '))
    if playing_robot == 'y':
        moves = '[@id="board-layout-sidebar"]/div'
        moves2 = 'board-vs-personalities'
    else:
        moves = '[@id="move-list"]'
        moves2 = 'board-single'
    best_speed = 0
    worst_speed = 99999999
    game_time = 0

    # Getting AI chess color
    while True:
        #ai_color = input("AI Color (w or b): ").lower()
        ai_color = 'w'
        if ai_color == "w" or ai_color == "b":
            break

    while board.is_checkmate() == False:
        print()
        print(board)
        if player(board) == ai_color:
            start_time = time.time()
            move = minimax(board, deep, cores)[0]
            end_time = time.time()
            tmp = str(move)
            print(type(move))
            print(tmp)
            is_capture = board.is_capture(move)
            en_passant = board.is_en_passant(move)
            move_num = moveto(tmp, move_num)
            board.push(move)
            total_time = round(end_time - start_time, 2)
            game_time += total_time
            approx_moves = board.legal_moves.count() ** (deep + 1)
            print(f"Approx Moves Searched: {approx_moves}")
            print("Time: " + str((total_time)))
            if approx_moves > 0:
                speed = approx_moves / (total_time+0.0001)
                if 100000 > speed > best_speed:
                    best_speed = speed
                if speed < worst_speed:
                    worst_speed = speed
                print(f'{speed} moves per second!')
                print(f'Best: {best_speed}')
                print(f'Worst: {worst_speed}')
        else:
            while True:
                element = WebDriverWait(driver, 100).until(

                EC.presence_of_element_located((By.XPATH, f'//*{moves}/vertical-move-list/div[{move_num}]/div[@class=\'black node selected\']'))

                )
                last_move = driver.find_element(By.XPATH, f'//*{moves}/vertical-move-list/div[{move_num}]/div[@class=\'black node selected\']')
                print(last_move.text)
                human_move = last_move.text
                try:
                    board.push_san(human_move)
                except:
                    continue
                break

    print("Checkmate")
    print(board)
    print(f'Total time thinking: {math.floor(game_time / 60)} mins {round(game_time - 60 * math.floor(game_time / 60))} secs.')
    input('Press Enter to Quit')
    driver.quit()

def moveto(name, move_num):
    import chess
    import time
    import math
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import multiprocessing
    from chessai import player, actions, result, evaluation, minimax, max_value, min_value, perform_minimax, board, cont
    columns = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}
    if name[-1] == 'q':
        promote = True
        name = name[:-1]
    else:
        promote = False
    start_location = name[-4:-2]
    end_location = name[-2:]
    piece = board.piece_at(chess.SQUARES[columns[start_location[0]]  - 1 + (int(start_location[1]) - 1) * 8])
    if piece.piece_type == 1:
        piece = 'p'
    elif piece.piece_type == 2:
        piece = 'n'
    elif piece.piece_type == 3:
        piece = 'b'
    elif piece.piece_type == 4:
        piece = 'r'
    elif piece.piece_type == 5:
        piece = 'q'
    elif piece.piece_type == 6:
        piece = 'k'
    print(piece)
    end_location = str(columns[end_location[0]]) + end_location[1]
    start_location = str(columns[start_location[0]]) + start_location[1]
    print(start_location, end_location)
    try:
        search = driver.find_element(By.XPATH, value = f'//*[@id="{moves2}"]/div[@class=\'piece w{piece} square-{start_location}\']')
    except: 
        search = driver.find_element(By.XPATH, value = f'//*[@id="{moves2}"]/div[@class=\'piece square-{start_location} w{piece}\']')
    search.click()
    if not is_capture:
        search = driver.find_element(By.XPATH, value = f'//*[@id="{moves2}"]/div[@class=\'hint square-{end_location}\']')
    else:
        if not en_passant:
            search = driver.find_element(By.XPATH, value = f'//*[@id="{moves2}"]/div[@class=\'capture-hint square-{end_location}\']')
        else:
            search = driver.find_element(By.XPATH, value = f'//*[@id="{moves2}"]/div[@class=\'hint square-{end_location}\']')
    action = webdriver.common.action_chains.ActionChains(driver)
    action.move_to_element_with_offset(search, 0, 0)
    action.click()
    if promote:
        driver.implicitly_wait(1)
        action.click()
    action.perform()
    move_num += 1
    return move_num

if __name__ == '__main__':
    main()