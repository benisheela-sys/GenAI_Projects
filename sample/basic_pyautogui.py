import pyautogui

#pause for 2 second
pyautogui.FAILSAFE =True
pyautogui.PAUSE=2.0

# Get screen size
width, height = pyautogui.size()
print(f"Screen Size: {width} x {height}")

# Current mouse position
print(pyautogui.position())

# Move mouse
pyautogui.moveTo(500, 300, duration=1)

# Click
pyautogui.click()

# Double click
pyautogui.doubleClick()

# Right click
pyautogui.rightClick()

# Type text
pyautogui.write("Hello World!", interval=0.1)

# Press Enter
pyautogui.press('enter')


