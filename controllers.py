import logging
from flask import request, json, url_for
from manage import app
from config import ENABLED_INFO_CLASSES, SEVER_STATUS_LIST
from utils import get_common_info, get_detail_server_info, get_detail_rack_info, create_rack, remove_rack, \
    create_and_add_server, add_server_to_rack, remove_server, sell_server, on_optical_port, move_to_del,\
    get_server_status, to_pay, doc_split

module_logger = logging.getLogger('main_log')


@app.route('/', methods=['GET'])
def index():
    available_url = {
        url_for('common_info'): doc_split(get_common_info.__doc__),
        url_for('server_info'): doc_split(get_detail_server_info.__doc__),
        url_for('rack_info'): doc_split(get_detail_rack_info.__doc__),
        url_for('new_rack'): doc_split(create_rack.__doc__),
        url_for('del_rack'): doc_split(remove_rack.__doc__),
        url_for('new_server'): doc_split(create_and_add_server.__doc__),
        url_for('move_server'): doc_split(add_server_to_rack.__doc__),
        url_for('del_server'): doc_split(remove_server.__doc__),
        url_for('to_delete'): doc_split(move_to_del.__doc__),
        url_for('sell'): doc_split(sell_server.__doc__),
        url_for('optical'): doc_split(on_optical_port.__doc__),
        url_for('get_status'): doc_split(get_server_status.__doc__),
        url_for('pay'): doc_split(to_pay.__doc__)
    }
    response = app.response_class(
        response=json.dumps(available_url),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/getinfo', methods=['POST'])
def common_info():
    if request.headers['Content-Type'] == 'application/json':
        content = request.get_json()
        date_true = False
        if 'sort_by_date' in content:
            date_true = True if content['sort_by_date'].lower() == 'true' else False
        if 'model_class' in content:
            if content['model_class'].lower() == ENABLED_INFO_CLASSES[0].lower():
                model = ENABLED_INFO_CLASSES[0]
            elif content['model_class'].lower() == ENABLED_INFO_CLASSES[1].lower():
                model = ENABLED_INFO_CLASSES[1]
            list_obj = get_common_info(model, date_true)
            result_request = {element.id: element.date_creation for element in list_obj}
        else:
            result_request = "Ошибка в указании класса модели."
    else:
        result_request = "Ошибка типа запроса."
    response = app.response_class(
        response=json.dumps(result_request),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/server/getinfo', methods=['POST'])
def server_info():
    if request.headers['Content-Type'] == 'application/json':
        content = request.get_json()
        if 'id' in content:
            result_request = get_detail_server_info(int(content['id']))
        else:
            result_request = "Ошибка в синтаксисе запроса."
    else:
        result_request = "Ошибка типа запроса."
    response = app.response_class(
        response=json.dumps(result_request),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/rack/getinfo', methods=['POST'])
def rack_info():
    if request.headers['Content-Type'] == 'application/json':
        content = request.get_json()
        if 'id' in content:
            result_request = get_detail_rack_info(int(content['id']))
        else:
            result_request = "Ошибка в синтаксисе запроса."
    else:
        result_request = "Ошибка типа запроса."
    response = app.response_class(
        response=json.dumps(result_request),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/rack/create', methods=['POST'])
def new_rack():
    if request.headers['Content-Type'] == 'application/json':
        content = request.get_json()
        if ('owner' in content) and ('volume' in content):
            result_request = create_rack(content['owner'], int(content['volume']))
            if not result_request:
                result_request = "Ошибка при создании серверной стойки."
        else:
            result_request = "Ошибка в синтаксисе запроса."
    else:
        result_request = "Ошибка типа запроса."
    response = app.response_class(
        response=json.dumps(result_request),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/rack/remove', methods=['POST'])
def del_rack():
    if request.headers['Content-Type'] == 'application/json':
        content = request.get_json()
        if 'id' in content:
            result_request = remove_rack(int(content['id']))
            if not result_request:
                result_request = "Ошибка - удаление стойки невозможно."
            else:
                result_request = "Серверная стойка удалена."
        else:
            result_request = "Ошибка в синтаксисе запроса."
    else:
        result_request = "Ошибка типа запроса."
    response = app.response_class(
        response=json.dumps(result_request),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/server/create', methods=['POST'])
def new_server():
    if request.headers['Content-Type'] == 'application/json':
        content = request.get_json()
        if ('rack_id' in content) and ('server_ip' in content) and ('ram' in content):
            result_request = create_and_add_server(int(content['rack_id']), content['server_ip'], int(content['ram']))
            if not result_request:
                result_request = "Ошибка при создании сервера."
        else:
            result_request = "Ошибка в синтаксисе запроса."
    else:
        result_request = "Ошибка типа запроса."
    response = app.response_class(
        response=json.dumps(result_request),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/server/move', methods=['POST'])
def move_server():
    if request.headers['Content-Type'] == 'application/json':
        content = request.get_json()
        if ('server_id' in content) and ('rack_id' in content):
            result_request = add_server_to_rack(int(content['server_id']), int(content['rack_id']))
            if not result_request:
                result_request = "Ошибка перемещения сервера."
            else:
                result_request = "Сервер с id %s успешно перемещен." % str(result_request)
        else:
            result_request = "Ошибка в синтаксисе запроса."
    else:
        result_request = "Ошибка типа запроса."
    response = app.response_class(
        response=json.dumps(result_request),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/server/remove', methods=['POST'])
def del_server():
    if request.headers['Content-Type'] == 'application/json':
        content = request.get_json()
        if 'id' in content:
            result_request = remove_server(int(content['id']))
            if not result_request:
                result_request = "Ошибка удаления сервера."
            else:
                result_request = "Сервер удален"
        else:
            result_request = "Ошибка в синтаксисе запроса."
    else:
        result_request = "Ошибка типа запроса."
    response = app.response_class(
        response=json.dumps(result_request),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/server/sell', methods=['POST'])
def sell():
    if request.headers['Content-Type'] == 'application/json':
        content = request.get_json()
        if ('id' in content) and ('new_operator' in content):
            result_request = sell_server(int(content['id']), str(content['new_operator']))
            if not result_request:
                result_request = "Ошибка операции продажи сервера."
            else:
                result_request = "Новый оператор сервера - %s." % str(content['new_operator'])
        else:
            result_request = "Ошибка в синтаксисе запроса."
    else:
        result_request = "Ошибка типа запроса."
    response = app.response_class(
        response=json.dumps(result_request),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/server/opticalport', methods=['POST'])
def optical():
    if request.headers['Content-Type'] == 'application/json':
        content = request.get_json()
        if 'id' in content:
            result_request = on_optical_port(int(content['id']))
            if not result_request:
                result_request = "Ошибка операции подключения оптического порта."
        else:
            result_request = "Ошибка в синтаксисе запроса."
    else:
        result_request = "Ошибка типа запроса."
    response = app.response_class(
        response=json.dumps(result_request),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/server/delete', methods=['POST'])
def to_delete():
    if request.headers['Content-Type'] == 'application/json':
        content = request.get_json()
        if 'id' in content:
            result_request = move_to_del(int(content['id']))
            if not result_request:
                result_request = "Ошибка операции переведения сервера в состояние %s." % SEVER_STATUS_LIST[-1]
            else:
                result_request = "Сервер успешно переведен в состояние %s." % SEVER_STATUS_LIST[-1]
        else:
            result_request = "Ошибка в синтаксисе запроса."
    else:
        result_request = "Ошибка типа запроса."
    response = app.response_class(
        response=json.dumps(result_request),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/server/status', methods=['POST'])
def get_status():
    if request.headers['Content-Type'] == 'application/json':
        content = request.get_json()
        if 'id' in content:
            result_request = get_server_status(int(content['id']))
            if not result_request:
                result_request = "Ошибка операции запроса состояния сервера."
        else:
            result_request = "Ошибка в синтаксисе запроса."
    else:
        result_request = "Ошибка типа запроса."
    response = app.response_class(
        response=json.dumps(result_request),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/server/pay', methods=['POST'])
def pay():
    if request.headers['Content-Type'] == 'application/json':
        content = request.get_json()
        if 'id' in content:
            result_request = to_pay(int(content['id']))
            if not result_request:
                result_request = "Ошибка операции оплаты сервера."
        else:
            result_request = "Ошибка в синтаксисе запроса."
    else:
        result_request = "Ошибка типа запроса."
    response = app.response_class(
        response=json.dumps(result_request),
        status=200,
        mimetype='application/json'
    )
    return response
