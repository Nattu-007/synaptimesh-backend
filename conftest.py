# conftest.py  ← place this in synaptimesh-backend/ (NOT inside tests/)
import sys
import os

# Adds the project root to Python path so 'app' is importable
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))