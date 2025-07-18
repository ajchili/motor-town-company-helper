import os
import sys
import time

import pyautogui
from tkinter.simpledialog import askstring
from tkinter.messagebox import askyesno, askquestion
from datetime import datetime, timedelta
import configparser

config = configparser.ConfigParser()
config.read("config.ini")
sleepTimer = 0.15

# Get current date and time
now = datetime.now()

# DEFAULT VALUES
PROMPT = os.getenv("PROMPT", default=config.get('Settings', 'prompt'))
WARNING_CALL = os.getenv("WARNING_CALL", default=config.get('Settings', 'WARNING_CALL'))
ONPATROL = os.getenv("ONPATROL", default=config.get('Settings', 'onPatrol'))
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
hornKey = config.get('gameKeys', 'hornKey')
roadSide = config.get('gameKeys', 'roadSideKey')
autopilot = config.get('gameKeys', 'autoPilotKey')

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

def press_key_longer(key: str) -> None:
	pyautogui.keyDown(key)
	time.sleep(1.50)
	pyautogui.keyUp(key)

def mouseClick(key: str) -> None:
	pyautogui.click(button=key)
	time.sleep(sleepTimer)

def refuelPatrolCar(onPatrol: int) -> None:
	if onPatrol == "True":
		time.sleep(sleepTimer)
		print("Officer on Patrol: Gonna stop autopilot and refuel vehicle")
		press_key(autopilot)
		time.sleep(sleepTimer)
		press_key_longer(selectionKey)
		time.sleep(sleepTimer)
		press_key(roadSide)
		time.sleep(sleepTimer)
		press_key(selectionKey)
		time.sleep(sleepTimer)
		press_key(selectionKey)
		time.sleep(90)
		press_key(autopilot)
		press_key(autopilot)
	else:
		print('No Patrol Car Available!')


def repair_company_vehicles(company_size: int) -> None:
	window = get_game_window()
	if not window.isActive:
		window.activate()
		# while True:
		# 	try:
		# 		window.activate()
		# 		# break
		# 	except Exception as err:
		# 		print(f"Game Not Found or game is not running: Error | {err=}, {type(err)=} ")
			

	if WARNING_CALL == "True":
		press_key_longer(hornKey)
		time.sleep(1)
		press_key_longer(hornKey)
		time.sleep(1)
		press_key_longer(hornKey)
		time.sleep(2)
	else:
		time.sleep(5)
		
	press_key(openCompanyUI)
	time.sleep(sleepTimer)
	press_key(downKey)
	time.sleep(sleepTimer)
	press_key(downKey)

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

def removeLines(number: int) -> None:
	for _ in range(number):
		# Move the cursor up one line
		sys.stdout.write('\033[F')
		# Clear the current line
		sys.stdout.write('\033[2K')


def prompt_for_repair() -> bool:
	result = askquestion(
		title="Repair Company Vehicle?",
		message="Would you like to repair your company vehicles now?"
	)

	return result == "Yes"


print(f"Running with variables {PROMPT=}, {COMPANY_SIZE=}, {REPAIR_INTERVAL=}, {WARNING_CALL=}, {ONPATROL=}")
try:
	while True:
		should_repair = True

		if PROMPT == "True":
			print("Prompting for repair...")
			should_repair = prompt_for_repair()


		if should_repair:
			# print(f"Repairing { COMPANY_SIZE } Vehicles Now")
			print(f"Mechanics are dispatched to { COMPANY_SIZE } Vehicles Now")
			
			refuelPatrolCar(onPatrol=ONPATROL)
			repair_company_vehicles(company_size=COMPANY_SIZE)

		for i in range(0, REPAIR_INTERVAL):
			# os.system('cls')

			print("Last repair time was:", now)
			# Add a specific number of Mins
			future_time_mins = now + timedelta(minutes=REPAIR_INTERVAL)
			print(f"Next Repair Time: ", future_time_mins)
			# print(f"Next Repair Time: (is in {REPAIR_INTERVAL - i} mins):", future_time_mins)

			# print(f"Waiting for {REPAIR_INTERVAL - i} more minutes before repairing again...")
			print(f"Mechanics are exchausted they repaired { COMPANY_SIZE } Vehicles and need rest. \nNext available mechanic in: { REPAIR_INTERVAL - i } minutes...")
			
			time.sleep(60)

			removeLines(4)
				
except KeyboardInterrupt:
	sys.exit(0)
# invoke-webrequest -Method Post -Uri 'http://192.168.1.50:12081/chat/?password=nothing&message="Good Message"' 