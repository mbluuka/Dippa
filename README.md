# ALSEC: controletor
Модуль проекта по автоматизированной настройке конфигурирования контролирования 
<!--Бейджи-->
:shipit:
![Static Badge](https://img.shields.io/badge/Mbluuka-ALSEContr-ALSEContr)
![GitHub top language](https://img.shields.io/github/languages/top/mbluuka/Dippa)
![GitHub Repo stars](https://img.shields.io/github/stars/mbluuka/Dippa)
:shipit:
<!--Описание-->
## Описание структуры 
Имеются 2 сценария сбора информации:
* PamInfoControl
* AstraSafePolicyControl

**Сценарий PamInfoControl** - сценарий Ansible предназначен для сбора информации о настройках безопасности паролей и аутентификации на серверах в ini-файле. Он анализирует файлы /etc/pam.d/common-password, /etc/pam.d/common-auth и /etc/login.defs, извлекает значения определенных параметров и сохраняет их в формате JSON как на удаленном сервере, так и локально.

**Сценарий AstraSafePolicyControl** - сценарий Ansible предназначен для сбора информации о настройках автологина и статусе Astra контролей на целевых хостах. Эта информация может быть использована для оценки безопасности системы и выявления потенциальных уязвимостей.

<!--Установка-->
## Установка (Linux)
1. Клонирование репозитория

```git clone https://github.com/mbluuka/Dippa.git```

2. Переход в директорию

```cd Dippa```

3. Запуск сценария

```ansible-playbook название_плейбука.yml --ask-become-pass```

4. Получение результата

После выполнения сценария следует перейти по директории `cd /etc/tmp/`, в которой Вы найдете JSON-файлы 
