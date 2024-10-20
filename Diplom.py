#!/usr/bin/python

import subprocess
import warnings
import json

warnings.simplefilter("ignore", DeprecationWarning)

# Функция для чтения конфигурационного файла login_defs
def get_login_defs():
    login_defs_info = {}

    try:
        with open('/etc/login.defs', 'r') as login_defs_config_file:
            for line in login_defs_config_file:
                if line.startswith('PASS_MIN_DAYS'):
                    login_defs_info['PASS_MIN_DAYS'] = line.split()[1]
                elif line.startswith('PASS_MAX_DAYS'):
                    login_defs_info['PASS_MAX_DAYS'] = line.split()[1]
                elif line.startswith('PASS_WARN_AGE'):
                    login_defs_info['PASS_WARN_AGE'] = line.split()[1]
                elif line.startswith('LOGIN_RETRIES'):
                    login_defs_info['LOGIN_RETRIES'] = line.split()[1]
                elif line.startswith('LOGIN_TIMEOUT'):
                    login_defs_info['LOGIN_TIMEOUT'] = line.split()[1]

    except Exception as e:
        return f"Возникла ошибка во время чтения файла login.defs: {str(e)}"

    return login_defs_info

# Функция для чтения конфигурационного файла о смене пароля
def get_chage_info(username):
    try:
        output = subprocess.check_output(['chage', '-l', username], stderr=subprocess.STDOUT, universal_newlines=True)
        return parse_chage_info(output.strip())
    except subprocess.CalledProcessError:
        return "Ошибка при получении информации о пароле."

def parse_chage_info(chage_output):
    chage_info = {}
    lines = chage_output.split('\n')
    for line in lines:
        if ':' in line:
            key, value = line.split(':', 1)  # Разделяем на ключ и значение
            chage_info[key.strip()] = value.strip()  # Убираем пробелы
    return chage_info

def get_firewall_info():
    try:
        output = subprocess.check_output(['iptables', '-L'], stderr=subprocess.STDOUT, universal_newlines=True)
        return output.strip()
    except subprocess.CalledProcessError:
        return "Ошибка при получении информации о файерволе."

def get_common_password_info():
    pam_cracklib_keyword = "pam_cracklib"
    file_to_check = "/etc/pam.d/common-password"
    parameter_info = []

    try:
        with open(file_to_check, 'r') as f:
            for line in f:
                if pam_cracklib_keyword in line:
                    parameters = line.strip().split()[3:]
                    param_dict = {}
                    for param in parameters:
                        key_value = param.split('=')
                        if len(key_value) == 2:
                            param_dict[key_value[0]] = key_value[1]
                    parameter_info.append(param_dict)
    except Exception as e:
        return f"Ошибка при проверке файла {file_to_check}: {str(e)}"

    if parameter_info:
        return parameter_info
    return "Шаблон pam_cracklib не найден в файле common-password."

def get_common_auth_info():
    file_to_check = "/etc/pam.d/common-auth"
    parameter_info = []
    deny_value = None

    try:
        with open(file_to_check, 'r') as f:
            for line in f:
                stripped_line = line.strip()
                if not stripped_line or stripped_line.startswith('#'):
                    continue

                parts = stripped_line.split()

                # Проверяем pam_tally.so и извлекаем deny
                if 'pam_tally.so' in parts:
                    for param in parts:
                        if param.startswith('deny='):
                            deny_value = param.split('=')[1]

                # Проверяем параметры pam_cracklib
                if 'pam_cracklib' in parts:
                    parameters = parts[3:]  # Пропускаем первые три элемента
                    param_dict = {}
                    for param in parameters:
                        if '=' in param:
                            key_value = param.split('=')
                            param_dict[key_value[0]] = key_value[1]
                    parameter_info.append(param_dict)

    except Exception as e:
        return f"Ошибка при проверке файла {file_to_check}: {str(e)}"

    if deny_value is not None:
        parameter_info.append({'deny': deny_value})

    if parameter_info:
        return parameter_info
    
    return "Шаблон pam_cracklib не найден в файле common-auth."

def export_to_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

if __name__ == "__main__":

    pam_password_info = get_common_password_info()
    pam_auth_info = get_common_auth_info()
    login_defs_info = get_login_defs()

    # Для более структурированного вывода login_defs
    if isinstance(login_defs_info, dict) and login_defs_info:
        print("\nНайдены параметры в login_defs:")
        for key, value in login_defs_info.items():
            print(f"{key}: {value}")
    else:
        print("\nНе удалось найти параметры в login_defs или файл пуст.")

    if isinstance(pam_password_info, list):
        print("\nНайдены параметры pam_cracklib в common-password:")
        for params in pam_password_info:
            for key, value in params.items():
                print(f"{key}: {value}")
    else:
        print(pam_password_info)

    if isinstance(pam_auth_info, list):
        print("\nНайдены параметры pam_cracklib в common-auth:")
        for params in pam_auth_info:
            for key, value in params.items():
                print(f"{key}: {value}")
    else:
        print(pam_auth_info)

    # Экспортируем данные в JSON
    export_to_json({
        'pam_cracklib_password': pam_password_info,
        'pam_cracklib_auth': pam_auth_info,
        'login_defs': login_defs_info,
    }, 'system_info.json')

    print("\nДанные успешно экспортированы в файл 'system_info.json'.")
