# slt-testtask
Приложение по управлению серверными стойками и серверами

Для запуска приложения, необходимо:
1. установить все зависимости виртуальной python3 среды из файла requirements.txt
2. активировать виртуальную среду с установленными ранее зависимостями
3. в терминале из директории с файлом manage.py запустить dev-сервер Flask:
    python manage.py
4. для получения информации по существующим url необходимо выполнить GET запрос по корневому url, казанному при старте
тестового сервера в п.3 (все указанные url принимают только POST запросы в формате json)
5. для проведения тестирования необходимо в директории с файлом testing.py и активированной виртуальной средой выполнить
запуск консольной команды:
    python testing.py

Список endpoint'ов:

* "/getinfo": "Получить краткую информацию по наличествующим стойкам. :param model_class: тип запрашиваемой модели (Rack | Server) :param sort_by_date: сортировать по дате (True | False) :return: Список стоек/серверов.",

* "/rack/create": "Создание пустой серверной стойки :param owner: Владелец (selectel | иной собственник) :param volume: Тип стойки (10 | 20) :return: id новой стойки",
    
* "/rack/getinfo": "Получение детальной информации по конкретной стойке :param id: целевой id :return: словарь значимых для серверной стойки параметров",

* "/rack/remove": "Удаление пустой стойки. :param id: идентификатор стойки :return: id удаленного срвера",

* "/server/create": "Создание нового сервера и добавление его в серверную стойку. :param rack_id: id стойки :param server_ip: назначенный ip :param ram: объем оперативной памяти :return: id созданного сервера",

* "/server/delete": "Перевести сервер в состояние Deleted :param id: целевой сервер :return: True",

* "/server/getinfo": "Получение детальной информации по серверу :param id: целевой id :return: словарь значимых для сервера параметров",

* "/server/move": "Добавление сервера в стойку :param server_id: сервер :param rack_id: id стойки куда перемещаем сервер :return: id",

* "/server/opticalport": "Включить оптический порт :param id: целевой id :return: True",

* "/server/pay": "Оплатить сервер :param id: целевой id :return: текущий статус сервера",

* "/server/remove": "Удаление сервера. :param id: целевой id :return: True",

* "/server/sell": "Продать сервер :param id: целевой id :param new_operator: новый пользователь :return: True",

* "/server/status": "Запрос состояния :param id: целевой сервер :return: статус сервера"
