import json

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


def export_to_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    parameter_info = get_common_password_info()

    # Для более структурированного вывода login_defs
    if isinstance(parameter_info, list):
        print("\nНайдены параметры pam_cracklib в common-password:")
        for params in parameter_info:
            for key, value in params.items():
                print(f"{key}: {value}")
    else:
        print(parameter_info)

    export_to_json({

        'common_password': parameter_info

    }, 'sys_info.json')
    