import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from shared.student import *

print(*IDENTIFIERS, sep=", ")
print(os.curdir)