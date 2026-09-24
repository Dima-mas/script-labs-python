"""
Завдання 1: Комплексний аналізатор надійності паролів
Реалізуйте програму, яка оцінює стійкість паролів користувача до компрометації.
Кроки виконання:
    1. Імпортуйте ваші персональні дані (ПІБ, варіант) з модуля shared/student.py.
    2. Завантажте вихідний список паролів та критерії згідно з вашим варіантом.
    3. Використовуючи стандартний модуль random, згенеруйте 3 випадкові індекси зі
        списку паролів, візьміть відповідні паролі та додайте їх дублікати в кінець
        початкового списку (таким чином імітується повторне використання паролів).
    4. Оцініть надійність кожного пароля за наступним алгоритмом:
        Заборонений: Якщо пароль входить до списку forbidden_passwords або
            його довжина менша за min_length з критеріїв.
        Слабкий: Якщо пароль не є забороненим і виконує хоча б один з критеріїв
            безпеки (містить хоча б одну цифру, велику літеру, спеціальний символ або
            малу літеру).
        Середній: Якщо пароль відповідає мінімальній довжині та деяким (але не всім)
            критеріям з різних груп символів.
        Сильний: Якщо пароль відповідає абсолютно всім критеріям безпеки
            (довжина, цифра, велика літера, спеціальний символ), але його довжина менша
            за min_length + 4 символів.
        Дуже сильний: Якщо пароль відповідає всім критеріям безпеки, має довжину
            min_length + 4 або більше символів, та є абсолютно унікальним у всьому
            списку паролів.
    5. Виведіть результат аналізу на екран у зручному табличному форматі."""

from random import randint as ran

passwords = [
    "UserPass1!",
    "temp",
    "Cyber$ecur1ty",
    "guest",
    "P0w3rful@Pass",
    "login",
    "Defens3#2023",
    "abc123",
    "Elit3@Secur",
    "demo",
]
criteria = {
    "min_length": 9,
    "require_digits": True,
    "require_lower"
    "require_upper": True,
    "require_special": True,
}
forbidden_passwords = {"temp", "guest", "login", "demo", "abc123", "user"}

repeats = (passwords[ran(0,len(passwords)-1)],
           passwords[ran(0,len(passwords)-1)],
           passwords[ran(0,len(passwords)-1)])
passwords.extend(repeats)

def check_password_validity(passwords:list[str], criteria:dict) -> list[tuple[str,str]]:
    statuses = []
    for password in passwords:
        criteria_passes = {
            "min_length": len(password) >= criteria["min_length"],
            "require_digits": any(digit in password for digit in "1234567890"),
            "require_upper": password.lower() != password,
            "require_special": any(symbol in password for symbol in " !\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~"),
        }
    
        is_very_strong = (all(criteria_passes.values()) 
                and len(password) >= criteria["min_length"] + 4
                and not passwords.count(password) > 1)
        is_strong = (all(criteria_passes.values()) 
                and len(password) >= criteria["min_length"] + 4)
        is_normal = (criteria_passes["min_length"]
                        and list(criteria_passes.values()).count(True) >= 2)
        is_weak = True in criteria_passes.values()
    
    
        if password in forbidden_passwords or not criteria_passes["min_length"]:
            statuses.append((password, "Заборонений"))
            continue
        else:
            if is_very_strong:
                statuses.append((password, "Дуже сильний"))
                continue
            elif is_strong:
                statuses.append((password, "Cильний"))
                continue
            elif is_normal:
                statuses.append((password, "Середній"))
                continue
            elif is_weak:
                statuses.append((password, "Слабкий"))
                continue
    return statuses


def execute():
    validated_passwords = check_password_validity(passwords, criteria)

    print("--------Завдання 1--------\nСтатуси паролів:")
    print(*[f"{status[0]}: {status[1]}" for status in validated_passwords], sep=";\n", end="\n\n")
            