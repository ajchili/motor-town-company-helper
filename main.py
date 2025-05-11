import os
import sys
import time

import pyautogui
import configparser

config = configparser.ConfigParser()
config.read("config.ini")
sleepTimer = 0.25

# DEFAULT VALUES
PROMPT = os.getenv("PROMPT", default=config.get('Settings', 'prompt'))
COMPANY_SIZE = int(os.getenv("COMPANY_SIZE", default=config.get('Settings', 'companySize')))
REPAIR_INTERVAL = int(os.getenv("REPAIR_INTERVAL", default=config.get('Settings', 'repairInterval')))

# GameKeys from the Config
openCompanyUI = config.get('gameKeys', 'companyUI')
downKey = config.get('gameKeys', 'downArrow')
upKey = config.get('gameKeys', 'upArrow')
leftKey = config.get('gameKeys', 'leftArrow')
rightKey = config.get('gameKeys', 'rightArrow')
selectionKey = config.get('gameKeys', 'spaceBar')
confimationKey = config.get('gameKeys', 'returnKey')
escapeKey = config.get('gameKeys', 'escapeKey')
mouseKeys = config.get('gameKeys', 'usingMouseButtonAsKeys')
interactionButton1 = config.get('gameKeys', 'Interact1')
interactionButton2 = config.get('gameKeys', 'Interact2')

if mouseKeys:
	if interactionButton1 == "LMB":
		interactionButton1 = 'left'
	else: 
		interactionButton1 = 'right'

	if interactionButton2 == "LMB":
		interactionButton2 = 'left'
	else:
		interactionButton2 = 'right'

class GameNotFoundError(Exception):
	pass


def get_game_window() -> pyautogui.Window:
	windows = pyautogui.getAllWindows()
	for window in windows:
		if "Motor Town" in window.title:
			return window

	raise GameNotFoundError()


def press_key(key: str) -> None:
	pyautogui.keyDown(key)
	time.sleep(sleepTimer)
	pyautogui.keyUp(key)

def mouseClick(key: str) -> None:
	pyautogui.click(button='left')
	time.sleep(sleepTimer)


def repair_company_vehicles(company_size: int) -> None:
	window = get_game_window()
	if not window.isActive:
		window.activate()
		time.sleep(sleepTimer)
		press_key(openCompanyUI)
		time.sleep(sleepTimer)
		press_key(downKey)
		time.sleep(sleepTimer)
		press_key(downKey)
		time.sleep(sleepTimer)

		for i in range(0, company_size):
			time.sleep(sleepTimer)
			press_key(selectionKey)
			time.sleep(sleepTimer)
			press_key(confimationKey)
			time.sleep(sleepTimer)
			press_key(downKey)
			time.sleep(sleepTimer)

		press_key(escapeKey)
		time.sleep(sleepTimer)
		


def prompt_for_repair() -> bool:
	result = pyautogui.confirm(
		title="Repair company vehicles?",
		text="Would you like to repair your company vehicles now?",
		buttons=("Yes", "No")
	)

	return result == "Yes"


print(f"Running with variables {PROMPT=}, {COMPANY_SIZE=}, {REPAIR_INTERVAL=}")
try:
	while True:
		should_repair = True

		if PROMPT == "True":
			print("Prompting for repair...")
			should_repair = prompt_for_repair()

		if should_repair:
				print(f"Repairing { COMPANY_SIZE } Vehicles Now")
				repair_company_vehicles(company_size=COMPANY_SIZE)

		for i in range(0, REPAIR_INTERVAL):
			print(f"Waiting for {REPAIR_INTERVAL - i} more minutes before repairing again...")
			time.sleep(60)
except KeyboardInterrupt:
	sys.exit(0)