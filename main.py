import os
import sys
import time

import pyautogui


PROMPT = os.getenv("PROMPT", default="False")
COMPANY_SIZE = int(os.getenv("COMPANY_SIZE", default="7"))
REPAIR_INTERVAL = int(os.getenv("REPAIR_INTERVAL", default="15"))


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
	pyautogui.keyUp(key)


def repair_company_vehicles(company_size: int) -> None:
	window = get_game_window()
	if not window.isActive:
		window.activate()
	
	press_key("o")
	press_key("down")
	press_key("down")

	for i in range(0, company_size):
		press_key("space")
		press_key("enter")
		press_key("down")

	press_key("esc")


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
				repair_company_vehicles(company_size=COMPANY_SIZE)

		for i in range(0, REPAIR_INTERVAL):
			print(f"Waiting for {REPAIR_INTERVAL - i} more minutes before repairing again...")
			time.sleep(60)
except KeyboardInterrupt:
	sys.exit(0)