import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from shared.student import *

import task1, task2, task3


print(f"{STUDENT_NAME}, {GROUP_NAME}, варіант №{VARIANT_NUMBER}")

input("task 1:\nProceed>")
task1.execute()
input("task 2:\nProceed>")
task2.execute()
input("task 3:\nProceed>")
task3.execute()