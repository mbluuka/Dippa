import json

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



def export_to_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    log_inf = get_login_defs()

    # Для более структурированного вывода login_defs
    if isinstance(log_inf, dict) and log_inf:
        print("\nНайдены параметры в login_defs:")
        for key, value in log_inf.items():
            print(f"{key}: {value}")
    else:
        print("\nНе удалось найти параметры в login_defs или файл пуст.")

    export_to_json({

        'login_defs': log_inf

    }, 'sys_info.json')
    