import json

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
    parameter_info = get_common_auth_info()

    # Для более структурированного вывода login_defs
    if isinstance(parameter_info, list):
        print("\nНайдены параметры pam_cracklib в common-auth:")
        for params in parameter_info:
            for key, value in params.items():
                print(f"{key}: {value}")
    else:
        print(parameter_info)

    export_to_json({

        'login_defs': parameter_info

    }, 'sys_info.json')
    