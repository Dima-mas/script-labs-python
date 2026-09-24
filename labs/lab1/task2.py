"""Завдання 2: Багаторівнева система контролю доступу
Розробіть прототип системи розмежування доступу користувачів до конфіденційних ресурсів.
Кроки виконання:
    1. Імпортуйте вхідні дані для свого варіанту (словник користувачів users, список
        ресурсів resources, рівні безпеки security_levels, множину заблокованих
        користувачів blocked_users).
    2. Виведіть список усіх ресурсів системи на екран, де числовий рівень безпеки ресурсу
        (від 1 до 4) замінено його текстовою назвою з кортежу security_levels
        (наприклад, замість 4 вивести Secret або Top Secret).
    3. Реалізуйте алгоритм перевірки доступу кожного користувача до кожного ресурсу.
        Алгоритм перевірки:
        Якщо користувача немає в системі (словнику users) -> DENY (User
            not found).
        Якщо користувач є у списку заблокованих blocked_users -> DENY
            (User is blocked).
        Якщо обліковий запис неактивний (active == False) -> DENY
            (Account inactive).
        Якщо числовий рівень допуску користувача (clearance) більший або
            дорівнює рівню безпеки ресурсу -> ALLOW.
        Якщо рівень допуску менший за рівень ресурсу -> DENY (Insufficient
            clearance).
    4. Виведіть результати перевірки на екран у форматі: user=[ім'я_користувача]
        resource=[назва_ресурсу] -> ALLOW / DENY ([причина_відмови])"""


users = {
    "security_chief": {
        "role": "security_officer",
        "clearance": 4,
        "department": "Security",
        "active": True,
    },
    "network_admin": {
        "role": "network_admin",
        "clearance": 3,
        "department": "Network",
        "active": True,
    },
    "help_desk": {
        "role": "support",
        "clearance": 1,
        "department": "Support",
        "active": True,
    },
    "auditor_ext": {
        "role": "auditor",
        "clearance": 3,
        "department": "Audit",
        "active": True,
    },
    "temp_worker": {
        "role": "temporary",
        "clearance": 1,
        "department": "Temp",
        "active": False,
    },
}
resources = [
    ("incident_reports", 4),
    ("network_topology", 3),
    ("user_manual", 1),
    ("vulnerability_scans", 3),
    ("root_access", 4),
    ("help_tickets", 1),
    ("penetration_tests", 4),
    ("firewall_rules", 3),
    ("software_licenses", 2),
    ("faq_docs", 1),
]
security_levels = ("Unrestricted", "Limited", "Sensitive", "Classified")
blocked_users = {"temp_worker", "fired_employee", "compromised_acc"}


def check_accesses(resources: tuple, users: dict) -> dict[str:dict]:
    access_dict = {user: {} for user in users.keys()}
    for user in users.keys():
        if not user in users.keys():
            access_dict[user].update(
                {res: "DENY (User not found)" for res in resources}
                )
            continue
        elif user in blocked_users:
            access_dict[user].update(
                {res: "DENY (User is blocked)" for res in resources}
                )
            continue
        elif users[user]["active"] == False:
            access_dict[user].update(
                {res: "DENY (Account inactive)" for res in resources}
                )
            continue
        for resource in resources:
            if users[user]["clearance"] < resource[1]:
                access_dict[user].update(
                    {resource: "DENY (Insufficient clearance)"}
                    )
            else:
                access_dict[user].update(
                    {resource: "ALLOW"}
                    )
    return access_dict
            


def execute():
    print("\nРесурси:")
    print(*[f"{resource[0]}: {security_levels[resource[1]-1]}" for resource in resources], sep="\n", end="\n\n\n")

    accesses_results = check_accesses(resources, users)
    results = []

    for user, val in accesses_results.items():
        for res, access in val.items():
            results.append(f"user={user}; resource={res[0]} -> {access}\n")
        results.append("\n\n")

    print(*results)