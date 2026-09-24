"""Завдання 3: Безпечне хешування, CSV-база та JSON-логування з винятками
Реалізуйте модуль для безпечної реєстрації та автентифікації користувачів, використовуючи
функції, декоратори та роботу з файлами.
Кроки виконання:
    1. Хешування: Створіть функцію generate_hash(password: str, salt: str
        = "00000") -> str.
        Функція має повертати шістнадцятковий хеш від конкатенації пароля та солі за
            допомогою алгоритму хешування з вашого варіанту.
        Якщо пароль або сіль порожні (None або "") — згенеруйте виняток
            ValueError.
        Якщо пароль коротший за мінімальну довжину з варіанту — згенеруйте
            власний виняток ValidationError (успадкований від Exception).
    2. Персональна сіль: Створіть сіль як рядок із 5 символів, що містить ваш варіант із
        shared/student.py, доповнений зліва нулями (наприклад, "00005" для 5
        варіанту).
    3. Реєстрація користувачів:
        Створіть кортеж users_to_register, що містить 10 записів (користувачів)
            у форматі (логін, пароль).
        Напишіть функцію create_user(username, password). Вона викликає
            generate_hash з вашою персональною сіллю та повертає кортеж
            (username, hash_value).
        Напишіть функцію create_users(users_list) для створення бази
            даних. Вона обробляє весь список користувачів та записує їх у файл
            labs/lab01/data/users.csv у форматі логін,хеш_пароля.
        Переконайтеся, що папка data створюється автоматично.
    4. Читання бази даних: Зчитайте вміст CSV-файлу у список users_db та виведіть
        його у вигляді структурованої таблиці на екран.
    5. Автентифікація: Напишіть функцію login(username: str, password:
        str) -> bool.
        Перевірте, чи існує користувач у users_db та чи збігається хеш введеного
            пароля (з урахуванням солі) з тим, що збережений у CSV.
        Якщо логін або пароль порожні — згенеруйте ValueError.
    6. Логування подій (Декоратор): Створіть декоратор @log_event, який записує
        кожну спробу входу у файл labs/lab01/data/log.json у форматі:
        {
        "event": "login",
        "user": "ім'я_користувача",
        "result": "success" или "failure",
        "timestamp": "YYYY-MM-DD HH:MM:SS",
        "args": [],
        "kwargs": {}
        }
    7. Обробка винятків: Увесь код роботи з файлами та входу обгорніть у блоки
        try...except із обробкою винятків: FileNotFoundError, PermissionError,
        IOError, ValidationError та ValueError.
    8. Організуйте весь запуск через головну функцію main()."""
    
# алгоритм хешування: sha1, мінімальна довжина пароля: 8    
import os
import sys
import csv
import json
import hashlib
from datetime import datetime
from functools import wraps

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from shared.student import VARIANT_NUMBER


data_dir = "labs/lab1/data"
password_min_length = 8
salt = f"0000{VARIANT_NUMBER}"

users_to_register = (
    ("Ddimcho", "dumbpassword"),
    ("Alina", "verysmartpassword"),
    ("Andrii4", "sans_undertale"),
    ("Andrii228", "dumbpassword"),
    ("Ostap", "Ebatb47"),
    ("Lazy_login", "lazypassword"),
    ("BroTan", "Sans_OuterSwap"),
    ("Lunekio", "Ki77yD1edY3ll0w"),
    ("Dwoe4ka", "Dota2"),
    ("Ddimcho2", "dumbpassword"),
)


   
    
def generate_hash(password: str, salt: str="00000") -> str:
    if password is None or password == "":
        raise ValueError("Password is empty")
    if salt is None or salt == "":
        raise ValueError("Salt is empty")
    if len(password) < password_min_length:
        raise ValidationError(f"Password should have at least {password_min_length} symbols.")

    data = password + salt
    hash_value = hashlib.sha1(data.encode("utf-8")).hexdigest()

    return hash_value


def create_user(username: str, password: str):
    if not username:
        raise ValueError("Empty login")
    
    hash_value = generate_hash(password, salt)
    return username, hash_value
    
        

def create_users(users_list:list[tuple]):
    try:
        with open(data_dir+"/users.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            for username, password in users_list:
                try:
                    user = create_user(username, password)
                    writer.writerow(user)

                except (ValueError, ValidationError) as e:
                    print(f"User Error '{username}': {e}")

    except (FileNotFoundError, PermissionError, IOError) as e:
        print(f"(handled at create_users) {type(e).__name__}: {e}")


def read_user_csv():
    users_db = []
    try:
        with open(data_dir+"/users.csv", "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 2:
                    username, password_hash = row
                    users_db.append({
                        "username": username,
                        "hash": password_hash
                        })
    except (FileNotFoundError, PermissionError, IOError) as e:
        print(f"(handled at read_user_csv) {type(e).__name__}: {e}")

    return users_db
        


def write_login_attempt(event):
    try:
        logs = []
        
        if os.path.isfile(data_dir+"/log.json"):
            try:
                with open(data_dir+"/log.json", "r", encoding="utf-8") as file:
                    logs = json.load(file)
                    if not isinstance(logs, list):
                        logs = []
            except json.JSONDecodeError:
                logs = []
        logs.append(event)

        with open(data_dir+"/log.json", "w", encoding="utf-8") as file:
            json.dump(logs, file, ensure_ascii=False, indent=4)
                
        

    except (FileNotFoundError, PermissionError, IOError) as e:
        print(f"(handled at write_login_attempt) {type(e).__name__}: {e}")


def log_event(function):
    @wraps(function)
    def record(*args, **kwargs):
        username = ""

        if len(args) > 0:
            username = args[0]
        elif "username" in kwargs:
            username = kwargs["username"]

        result = "failure"

        try:
            success = function(*args, **kwargs)

            if success:
                result = "success"

            return success

        except (ValueError, ValidationError):
            # Помилка входу також вважається невдалою спробою
            result = "failure"
            raise

        finally:
            event = {
                "event": "login",
                "user": username,
                "result": result,
                "timestamp": datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "args": [],
                "kwargs": {}
            }

            write_login_attempt(event)

    return record
        

@log_event
def login(username: str, password: str) -> bool:
    if username is None or username == "":
        raise ValueError("Username is empty")
    if password is None or password == "":
        raise ValueError("Password is empty")

    try:
        users_db = read_user_csv()

        for user in users_db:
            if user["username"] == username:
                input_hash = generate_hash(password, salt)
                if input_hash == user["hash"]:
                    return True
                return False
        return False

    except (FileNotFoundError, PermissionError, IOError, ValidationError, ValueError) as e:
        print(f"(handled at login) {type(e).__name__}: {e}")
        return False


class ValidationError(Exception):
    pass




def execute():
    os.makedirs(os.path.dirname("labs/lab1/data"), exist_ok=True)

    
    print("Creating users db...")
    try:
        create_users(users_to_register)
        print("Users db created✅")

    except (FileNotFoundError, PermissionError, IOError, ValidationError, ValueError) as e:
        print(f"(handled at execute > creating users db) {type(e).__name__}: {e}")


    print("Reading users db...")
    try:
        print("User db read succesfully✅")
    except (FileNotFoundError, PermissionError, IOError, ValidationError, ValueError) as e:
        print(f"(handled at execute > reading users db) {type(e).__name__}: {e}")


    print("Logging in...")
    
    
    print("Succesful try:")
    try:
        result = login("Ddimcho", "dumbpassword")
        if result:
            print("Ddimcho: Logged in succesfully")
        else:
            print("Ddimcho: Login failed")
    except (ValueError, ValidationError) as e:
        print(f"(handled at execute > reading users db) {type(e).__name__}: {e}")


    print("Failed try:")
    try:
        result = login("Ddimcho2", "dumbpassword(not correct obviously)")
        if result:
            print("Ddimcho2: Logged in succesfully")
        else:
            print("Ddimcho2: Login failed")
    except (ValueError, ValidationError) as e:
        print(f"(handled at execute) {type(e).__name__}: {e}")


    print("\n\n-----------------------------------------------------------\n")
    print(f"Users table:\n{'№':<5}{'Логін':<20}{'SHA-1 хеш':<40}")
    for number, user in enumerate(read_user_csv(), start=1):
        print(f"{number:<5}{user['username']:<20}{user['hash']:<40}")