import os
import argparse
from datetime import datetime
import logging

'''
Python script to help me manage SRT files. Rose out a need to replace a bunch of mis-encoded characters.
Takes a directory, and then the string to find and what to replace it with. Other options are below.
'''

parser = argparse.ArgumentParser(description = "Utility to help manage SRT files. Default behavior is converting &gt; to >.",
								 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("-d", "--dry-run", action="store_true", help="test run of the script. does not modify files.")
parser.add_argument("-l", "--logging", action="store_true", help="Turn on logging. Log written at src.")
parser.add_argument("src", help="Source location")
parser.add_argument("old", type=str, help ="Text to be replaced.")
parser.add_argument("new", type=str, help ="Replacement text")
args = parser.parse_args()
config = vars(args)

src = config['src']
old = config['old']
new = config['new']
dry_run = config['dry_run']
log_on = config['logging']

if log_on:
	start_time = datetime.now()
	str_time = start_time.strftime("%y-%m-%d_%H-%M-%S")
	log_path = os.path.join(src, "log\\")
	log_filename = str_time + ".log"
	os.makedirs(log_path) if not os.path.exists(log_path) else None
	logging.basicConfig(filename=log_path+log_filename, encoding='utf-8', level=logging.DEBUG,
						format='%(asctime)s:%(levelname)s %(message)s')

	logging.info(config)	
	
def replace_improper_markers(file, old, new):
	with open(file, mode="r+", encoding = "UTF8") as f:
		t = f.read()
		updated = t.replace(old, new)
		f.seek(0)
		f.write(updated)
		f.close()

if not dry_run:
	for root, dirs, files in os.walk(src):
		if logging: logging.info(f"Root: {root}")
		for file in files:
			if file.endswith(".srt"):
				if log_on: logging.info(f"{os.path.join(root,file)} is being processed.")
				replace_improper_markers(os.path.join(root, file), old, new)
				if log_on:logging.info(f"{os.path.join(root,file)}")

else:
	if log_on: logging.info("Starting dry run.")
	files_to_modify = []
	for root, dirs, files in os.walk(src):
		for file in files:
			if file.endswith(".srt"):
				files_to_modify += [os.path.join(root, file)]
	if log_on: logging.info(files_to_modify)
	
if log_on: logging.info(f"Completed edits. Total time: {datetime.now() - start_time}")