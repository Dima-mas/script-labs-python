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
    
def generate_hash(password: str, salt: str="00000") -> str:
    pass

def create_user(username, password):
    pass

def create_users(users_list):
    pass


def log_event(function):
    def record(user, pas):
        pass
        

@log_event
def login(username: str, password: str) -> bool:
    pass


class ValidationError(Exception):
    pass



try:
    length = 9
    if not length >= 8:
        raise ValidationError("ValidationError: the password is too short")
except FileNotFoundError, PermissionError, IOError, ValueError:
    pass
except ValidationError as e:
    print(f"An error has occured: {e}")