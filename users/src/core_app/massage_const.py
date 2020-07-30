VALUE_ERR = {'response': 'BAD_REQUEST',
             'massage': '',
             'help': 'Необходимый формат: {"username": int, "password": str, "email": str}'}

DUPLICATE_VALUE = {'response': 'BAD_REQUEST',
                   'massage': 'Пользователь с таким имененм уже существует',
                   'help': 'Измените имя пользователя'}

INSERT_DB_ERR = {'response': 'ERROR',
                 'massage': 'В процессе что-то пошло не так'}

INSERT_DB_SUCCESS = {'response': 'OK',
                     'massage': 'Пользователь успешно зарегистрирован'}

INCORRECT_PASS = {'response': 'BAD_REQUEST',
                  'massage': 'Неверный пароль'}

INCORRECT_USERNAME = {'response': 'BAD_REQUEST',
                      'massage': 'Пользователь не найден'}