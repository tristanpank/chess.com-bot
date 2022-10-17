import chess
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


s = Service("C:/Users/trist/anaconda3/chromedriver")

driver = webdriver.Chrome(service = s)

driver.get("https://www.chess.com/login")
search = driver.find_element(By.XPATH, value='//*[@id="username"]')
search.send_keys('Dekshunari2')

search = driver.find_element(By.ID, value='password')
search.send_keys('Dek$hunari057')
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
def moveto(name):
    global move_num
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
    search = driver.find_element(By.XPATH, value = f'//*[@id="board-vs-personalities"]/div[@class=\'piece w{piece} square-{start_location}\']')
    search.click()
    if not is_capture:
        search = driver.find_element(By.XPATH, value = f'//*[@id="board-vs-personalities"]/div[@class=\'hint square-{end_location}\']')
    else:
        try:
            search = driver.find_element(By.XPATH, value = f'//*[@id="board-vs-personalities"]/div[@class=\'capture-hint square-{end_location}\']')
        except:
            search = driver.find_element(By.XPATH, value = f'//*[@id="board-vs-personalities"]/div[@class=\'hint square-{end_location}\']')
    action = webdriver.common.action_chains.ActionChains(driver)
    action.move_to_element_with_offset(search, 0, 0)
    action.click()
    if promote:
        driver.implicitly_wait(1)
        action.click()
    action.perform()
    move_num += 1

board = chess.Board()

from chessai import player, actions, result, evaluation, minimax, max_value, min_value


# Getting AI chess color
while True:
    ai_color = input("AI Color (w or b): ").lower()
    if ai_color == "w" or ai_color == "b":
        break

while board.is_checkmate() == False:
    print()
    print(board)
    if player(board) == ai_color:
        start_time = time.time()
        move = minimax(board, 4)
        tmp = str(move)
        is_capture = board.is_capture(move)
        print(tmp)
        moveto(tmp)
        board.push(move)
        end_time = time.time()
        total_time = round(end_time - start_time, 2)
        print("Time: " + str((total_time)))
    else:
        while True:
            element = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.XPATH, f'//*[@id="board-layout-sidebar"]/div/vertical-move-list/div[{move_num}]/div[@class=\'black node selected\']'))
            )
            last_move = driver.find_element(By.XPATH, f'//*[@id="board-layout-sidebar"]/div/vertical-move-list/div[{move_num}]/div[@class=\'black node selected\']')
            print(last_move.text)
            human_move = last_move.text
            try:
                board.push_san(human_move)
            except:
                continue
            break

print("Checkmate")
print(board)
input('Press Enter to Quit')
driver.quit()
