from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
s  = Service("/usr/local/bin/chromedriver")

driver = webdriver.Chrome(service = s)

driver.get("https://www.chess.com/login")
search = driver.find_element(By.XPATH, value='//*[@id="username"]')
search.send_keys('Dekshunari2')

search = driver.find_element(By.ID, value='password')
search.send_keys('Dek$hunari057')
search = driver.find_element(By.ID, value = 'login')
search.click()
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
    EC.presence_of_element_located((By.XPATH, '//*[@id="board-layout-sidebar"]/div/div[2]/div/div[4]/div/div[2]/div/div[3]/div[2]/button[3]'))
)
search = driver.find_element(By.XPATH, value = '//*[@id="board-layout-sidebar"]/div/div[2]/div/div[4]/div/div[2]/div/div[3]/div[2]/button[3]')
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
 
driver.implicitly_wait(20)
move = 0
def moveto(piece, start_location, end_location, capture = False):
    global move
    columns = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}
    end_location = str(columns[end_location[0]]) + end_location[1]
    start_location = str(columns[start_location[0]]) + start_location[1]
    print(start_location, end_location)
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f'//*[@id="board-single"]/div[@class=\'piece w{piece} square-{start_location}\']'))
    )
    search = driver.find_element(By.XPATH, value = f'//*[@id="board-single"]/div[@class=\'piece w{piece} square-{start_location}\']')
    search.click()
    if not capture:
        search = driver.find_element(By.XPATH, value = f'//*[@id="board-single"]/div[@class=\'hint square-{end_location}\']')
    else:
        search = driver.find_element(By.XPATH, value = f'//*[@id="board-single"]/div[@class=\'capture-hint square-{end_location}\']')
    action = webdriver.common.action_chains.ActionChains(driver)
    action.move_to_element_with_offset(search, 0, 0)
    action.click()
    action.perform()
    move += 1

while True:
    moveto(input('Piece: '), input("\nStart: "), input('\nEnd:'), input('\nTakes? '))
    print()
    element = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.XPATH, f'//*[@id="move-list"]/vertical-move-list/div[{move}]/div[3]'))
        )
    last_move = driver.find_element(By.XPATH, f'//*[@id="move-list"]/vertical-move-list/div[{move}]/div[3]')
    print(last_move.text)
        