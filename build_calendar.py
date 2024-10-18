import subprocess
import os
print("This is the OS CWD:" + os.getcwd())
# Define the path to the Python interpreter in your virtual environment
python_interpreter = "/Users/danielvm/Sites/ics-files-1/venv/bin/python"

# Call scrape_flashscore.py
try:
	subprocess.call([python_interpreter, "src/scrape_flashscore.py"])
	print("Finished the scrape of the next matches!")
except Exception as e:
	print(f"Error: {e}")

# Call scrape_flashscore_past.py
try:
	subprocess.call([python_interpreter, "src/scrape_flashscore_past.py"])
	print("Finished the scrape of the past matches!")
except Exception as e:
	print(f"Error: {e}")

# Call create_ics_full.py
try:
	subprocess.call([python_interpreter, "src/create_ics_full.py"])
	print("Finished creating the full calendar!")
except Exception as e:
	print(f"Error: {e}")