# tests/conftest.py
import sys, os

# insert the project root (one level up) so that "import src" works
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
