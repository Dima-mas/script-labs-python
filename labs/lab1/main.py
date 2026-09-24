import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import task1
import task2
import task3

from shared.student import *

print(f"{STUDENT_NAME}, {GROUP_NAME}, варіант №{VARIANT_NUMBER}")

input("task 1:\nProceed>")
task1.execute()
input("task 2:\nProceed>")
task2.execute()
input("task 3:\nProceed>")
task3.execute()