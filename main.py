import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import bcrypt
import jwt  
import datetime
import json

# Конфигурации
JWT_SECRET = 'your-very-secret-key'
JWT_ALGORITHM = 'HS256'

# Инициализация Flask приложения
app = Flask(__name__)

# Настройка CORS
CORS(app)

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Функция для загрузки конфигурации из JSON файла
def load_db_config():
    try:
        with open('config.json', 'r', encoding='utf-8') as config_file:
            config = json.load(config_file)
            logger.debug('Конфигурация базы данных успешно загружена из config.json')
            return config
    except FileNotFoundError:
        logger.error('Файл config.json не найден')
        raise
    except json.JSONDecodeError as e:
        logger.error(f'Ошибка парсинга config.json: {e}')
        raise
    except Exception as e:
        logger.error(f'Неизвестная ошибка при загрузке конфигурации: {e}')
        raise

# Загружаем конфигурацию БД
try:
    DB_CONFIG = load_db_config()
except Exception as e:
    logger.error(f'Не удалось загрузить конфигурацию БД: {e}')
    # Можно установить значения по умолчанию или завершить работу
    DB_CONFIG = {}

# Установка соединения с PostgreSQL
def get_db_connection():
    logger.debug('Попытка подключения к базе данных...')
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        logger.debug('Подключение к базе данных успешно установлено')
        return conn
    except Exception as e:
        logger.error(f"Ошибка подключения к базе данных: {e}")
        # Возвращаем более детальную ошибку для отладки
        return None

# Глобальный обработчик CORS
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://127.0.0.1:5500')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

# Регистрация компании
@app.route('/api/worki-auth/company-registration', methods=['POST'])
def registerCompany():
    data = request.get_json()
    if not data:
        logger.warning('Не получены JSON данные для регистрации')
        return jsonify({'error': 'Не получены JSON данные'}), 400

    login = data.get('login')
    password = data.get('password')
    name = data.get('name')
    fullName = data.get('fullName')
    status = False

    logger.debug(f"Попытка регистрации компании - Название компании: {name}")

    # Проверка обязательных полей
    if not all([login, password, name, fullName]):
        logger.warning('Отсутствуют обязательные поля при регистрации')
        return jsonify({'error': 'Отсутствуют обязательные поля'}), 400

    # Подключаемся к БД
    conn = get_db_connection()
    if conn is None:
        logger.error("Не удалось подключиться к базе данных")
        return jsonify({'error': 'Ошибка подключения к базе данных'}), 500
        
    cur = conn.cursor()
    
    try:
        # Проверяем, существует ли уже пользователь с таким логином
        cur.execute('SELECT "Login" FROM "Companies" WHERE "Login" = %s', (login,))
        if cur.fetchone():
            logger.warning(f"Компания с логином {login} уже существует")
            return jsonify({'error': 'Логин компании уже существует'}), 400
        
        # Хешируем пароль
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        cur.execute(''' 
            INSERT INTO "Companies" ("Login", "Name", "FullName", "Password", "Password(tesing)", "Status") 
            VALUES (%s, %s, %s, %s, %s, %s) 
        ''', (login, name, fullName, password_hash, password, status))

        conn.commit()
        logger.info(f"Компания {name} успешно зарегистрирована")

        return jsonify({'message': 'Компания успешно зарегистрирована'}), 201

    except Exception as e:
        logger.error(f"Произошла ошибка при регистрации: {e}")
        conn.rollback()
        return jsonify({'error': 'Произошла внутренняя ошибка'}), 500

    finally:
        cur.close()
        conn.close()
        logger.debug("Соединение с базой данных закрыто")

# Регистрация университета
@app.route('/api/worki-auth/uni-registration', methods=['POST'])
def registerUni():
    data = request.get_json()
    if not data:
        logger.warning('Не получены JSON данные для регистрации')
        return jsonify({'error': 'Не получены JSON данные'}), 400

    login = data.get('login')
    password = data.get('password')
    name = data.get('name')
    fullName = data.get('fullName')
    status = False

    logger.debug(f"Попытка регистрации университета - Название университета: {name}")

    # Проверка обязательных полей
    if not all([login, password, name, fullName]):
        logger.warning('Отсутствуют обязательные поля при регистрации')
        return jsonify({'error': 'Отсутствуют обязательные поля'}), 400

    # Подключаемся к БД
    conn = get_db_connection()
    if conn is None:
        logger.error("Не удалось подключиться к базе данных")
        return jsonify({'error': 'Ошибка подключения к базе данных'}), 500
        
    cur = conn.cursor()
    
    try:
        # Проверяем, существует ли уже университет с таким email
        cur.execute('SELECT "Email" FROM "Unis" WHERE "Email" = %s', (login,))
        if cur.fetchone():
            logger.warning(f"Университет с email {login} уже существует")
            return jsonify({'error': 'Email университета уже существует'}), 400
        
        # Хешируем пароль
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        cur.execute(''' 
            INSERT INTO "Unis" ("Email", "Name", "FullName", "Password", "Password(tesing)", "Status") 
            VALUES (%s, %s, %s, %s, %s, %s) 
        ''', (login, name, fullName, password_hash, password, status))

        conn.commit()
        logger.info(f"Университет {name} успешно зарегистрирован")

        return jsonify({'message': 'Университет успешно зарегистрирован'}), 201

    except Exception as e:
        logger.error(f"Произошла ошибка при регистрации: {e}")
        conn.rollback()
        return jsonify({'error': 'Произошла внутренняя ошибка'}), 500

    finally:
        cur.close()
        conn.close()
        logger.debug("Соединение с базой данных закрыто")

# Вход для сотрудника компании
@app.route('/api/worki-auth/company-worker-login', methods=['POST'])
def CompanyWorkerlogin():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Не получены JSON данные'}), 400
        
    login = data.get('login')
    password = data.get('password')

    if not login or not password:
        return jsonify({'error': 'Требуется имя сотрудника компании и пароль'}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Ошибка подключения к базе данных'}), 500
        
    cur = conn.cursor()

    try:
        # Ищем пользователя в таблице Companies
        cur.execute('SELECT * FROM "Companies" WHERE "Name" = %s', (login,))
        user = cur.fetchone()
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
            # Создаем JWT токен
            token_payload = {
                'user_id': user[0],
                'username': user[0],    
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            }
            
            # Используем jwt.encode с правильными параметрами
            token = jwt.encode(
                token_payload, 
                JWT_SECRET, 
                algorithm=JWT_ALGORITHM
            )

            # Если используется PyJWT >= 2.0.0, токен может быть в bytes, декодируем в строку
            if isinstance(token, bytes):
                token = token.decode('utf-8')

            user_data = {
                'Name': user[0],
            }

            return jsonify({
                'message': 'Вход выполнен успешно',
                'token': token,
                'user': user_data
            }), 200
        else:
            return jsonify({'error': 'Неверное имя пользователя или пароль'}), 401

    except Exception as e:
        logger.error(f"Ошибка входа: {e}")
        return jsonify({'error': 'Внутренняя ошибка сервера'}), 500
    finally:
        cur.close()
        conn.close()
        
# Вход для представителя университета
@app.route('/api/worki-auth/uni-login', methods=['POST'])
def Unilogin():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Не получены JSON данные'}), 400
        
    login = data.get('login')
    password = data.get('password')

    if not login or not password:
        return jsonify({'error': 'Требуется email и пароль университета'}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Ошибка подключения к базе данных'}), 500
        
    cur = conn.cursor()

    try:
        # Ищем пользователя в таблице Unis
        cur.execute('SELECT * FROM "Unis" WHERE "Email" = %s', (login,))
        user = cur.fetchone()
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):
            # Создаем JWT токен
            token_payload = {
                'user_id': user[0],
                'username': user[0],    
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            }
            
            # Используем jwt.encode с правильными параметрами
            token = jwt.encode(
                token_payload, 
                JWT_SECRET, 
                algorithm=JWT_ALGORITHM
            )

            # Если используется PyJWT >= 2.0.0, токен может быть в bytes, декодируем в строку
            if isinstance(token, bytes):
                token = token.decode('utf-8')

            user_data = {
                'Name': user[0],
            }

            return jsonify({
                'message': 'Вход выполнен успешно',
                'token': token,
                'user': user_data
            }), 200
        else:
            return jsonify({'error': 'Неверное имя пользователя или пароль'}), 401

    except Exception as e:
        logger.error(f"Ошибка входа: {e}")
        return jsonify({'error': 'Внутренняя ошибка сервера'}), 500
    finally:
        cur.close()
        conn.close()

# Создание вакансий
@app.route('/api/worki-auth/vacancy-creation', methods=['POST'])
def vacancyCreation():
    data = request.get_json()
    if not data:
        logger.warning('Не получены JSON данные для создания вакансии')
        return jsonify({'error': 'Не получены JSON данные'}), 400

    companyName = data.get('companyName')
    Name = data.get('Name')
    Description = data.get('Description')
    Status = data.get('Status')
    CampusName = data.get('CampusName')
    Type = data.get('Type')
    Salary = data.get('Salary')
    if Salary == '': Salary = '0'

    logger.debug(f"Попытка создания вакансии")

    # Проверка обязательных полей
    if not all([companyName, Name, Description, Status, CampusName, Type]):
        logger.warning('Отсутствуют обязательные поля при создании вакансии')
        return jsonify({'error': 'Отсутствуют обязательные поля'}), 400

    # Подключаемся к БД
    conn = get_db_connection()
    if conn is None:
        logger.error("Не удалось подключиться к базе данных")
        return jsonify({'error': 'Ошибка подключения к базе данных'}), 500
        
    cur = conn.cursor()

    try:
        cur.execute(''' 
            INSERT INTO "Vacancies" ("CompanyName", "Name", "Description", "Status", "CampusName", "Type", "Salary") 
            VALUES (%s, %s, %s, %s, %s, %s, %s) 
        ''', (companyName, Name, Description, Status, CampusName, Type, Salary))

        conn.commit()
        logger.info(f"Вакансия {Name} успешно создана")

        return jsonify({'message': 'Вакансия успешно создана'}), 201

    except Exception as e:
        logger.error(f"Произошла ошибка при создании вакансии: {e}")
        conn.rollback()
        return jsonify({'error': 'Произошла внутренняя ошибка'}), 500

    finally:
        cur.close()
        conn.close()
        logger.debug("Соединение с базой данных закрыто")

# Данные для HR
@app.route('/api/worki-auth/hr-data', methods=['GET'])
def get_resume_data():
    token = request.headers.get('Authorization')
    
    if not token or not token.startswith('Bearer '):
        return jsonify({'error': 'Требуется токен'}), 401

    try:
        token = token.split(' ')[1]
        # Используем метод decode из PyJWT
        payload = jwt.decode(
            token, 
            JWT_SECRET, 
            algorithms=[JWT_ALGORITHM]
        )
        
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute('SELECT * FROM "Vacancies" WHERE "Login" = %s', (payload['Name'],))
        user = cur.fetchone()
        
        if user:
            user_data = {
                'Name': user[2],
                'Description': user[3],
                'Status': user[4],
                'CampusName': user[5],
                'Type': user[6], 
                'Salary': user[7]
            }
            return jsonify(user_data), 200
        else:
            return jsonify({'error': 'Пользователь не найден'}), 404
            
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Срок действия токена истек'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Недействительный токен'}), 401
    except Exception as e:
        logger.error(f"Ошибка получения данных: {e}")
        return jsonify({'error': 'Внутренняя ошибка сервера'}), 500
    finally:
        cur.close()
        conn.close()

# Данные по типам вакансий
@app.route('/api/worki-auth/get-vacancy-types', methods=['GET'])
def get_vancany_types_data():
    try:        
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute('SELECT * FROM "VacancyTypes" ')
        types = cur.fetchall()
        if types:
            types_data = {
                'Name': [x[0] for x in types],
                'Description': [x[1] for x in types]
            }
            return jsonify(types_data), 200
        else:
            return jsonify({'error': "Типы вакансий недоступны по какой-то причине........."}), 404
            
    except Exception as e:
        logger.error(f"Ошибка получения данных: {e}")
        return jsonify({'error': 'Внутренняя ошибка сервера'}), 500
    finally:
        cur.close()
        conn.close()

# Данные по статусам вакансий
@app.route('/api/worki-auth/get-vacancy-statuses', methods=['GET'])
def get_vancany_statuses_data():
    try:        
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute('SELECT * FROM "VacancyStatuses" ')
        statuses = cur.fetchall()
        if statuses:
            statuses_data = {
                'Name': [x[0] for x in statuses],
                'Description': [x[1] for x in statuses]
            }
            return jsonify(statuses_data), 200
        else:
            return jsonify({'error': "Статусы вакансий недоступны по какой-то причине........."}), 404
            
    except Exception as e:
        logger.error(f"Ошибка получения данных: {e}")
        return jsonify({'error': 'Внутренняя ошибка сервера'}), 500
    finally:
        cur.close()
        conn.close()

# Данные по площадкам
@app.route('/api/worki-auth/get-campuses', methods=['GET'])
def get_vancany_campuses():
    try:        
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute('SELECT * FROM "Campuses" ')
        campuses = cur.fetchall()
        if campuses:
            campuses_data = {
                'Name': [x[0] for x in campuses],
                'Location': [x[1] for x in campuses],
                'FullName': [x[2] for x in campuses]
            }
            return jsonify(campuses_data), 200
        else:
            return jsonify({'error': "Данные по площадкам недоступны по какой-то причине........."}), 404
            
    except Exception as e:
        logger.error(f"Ошибка получения данных: {e}")
        return jsonify({'error': 'Внутренняя ошибка сервера'}), 500
    finally:
        cur.close()
        conn.close()

# Данные по компаниям
@app.route('/api/worki-auth/get-companies', methods=['GET'])
def get_companies():
    try:        
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute('SELECT * FROM "Companies" ')
        companies = cur.fetchall()
        if companies:
            companies_data = {
                'Name': [x[0] for x in companies],
                'FullName': [x[1] for x in companies],
            }
            return jsonify(companies_data), 200
        else:
            return jsonify({'error': "Данные по компаниям недоступны по какой-то причине........."}), 404
            
    except Exception as e:
        logger.error(f"Ошибка получения данных: {e}")
        return jsonify({'error': 'Внутренняя ошибка сервера'}), 500
    finally:
        cur.close()
        conn.close()

# Данные по университетам
@app.route('/api/worki-auth/get-unis', methods=['GET'])
def get_unis():
    try:        
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute('SELECT * FROM "Unis" ')
        unis = cur.fetchall()
        if unis:
            unis_data = {
                'Email': [x[0] for x in unis],
                'Name': [x[2] for x in unis],
                'FullName': [x[3] for x in unis],
                'Status': [x[4] for x in unis],
            }
            return jsonify(unis_data), 200
        else:
            return jsonify({'error': "Данные по университетам недоступны по какой-то причине........."}), 404
            
    except Exception as e:
        logger.error(f"Ошибка получения данных: {e}")
        return jsonify({'error': 'Внутренняя ошибка сервера'}), 500
    finally:
        cur.close()
        conn.close()

# Для запуска локально
if __name__ == '__main__':
    logger.info("Запуск Flask приложения на http://0.0.0.0:5002")
    app.run(host='0.0.0.0', port=5002, debug=True)