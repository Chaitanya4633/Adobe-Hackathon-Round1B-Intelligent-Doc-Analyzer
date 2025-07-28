config.py
import os

INPUT_DIR = "/app/input"
OUTPUT_DIR = "/app/output"

if not os.path.exists(INPUT_DIR):
    INPUT_DIR = "../input"
if not os.path.exists(OUTPUT_DIR):
    OUTPUT_DIR = "../output"

MAX_TITLE_LENGTH = 150
MIN_HEADING_LENGTH = 2
MAX_HEADING_LENGTH = 200