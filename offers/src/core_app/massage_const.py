VALUE_ERR = {'response': 'BAD_REQUEST',
             'massage': '',
             'help': 'Необходимый формат: {"user_id": int, "title": str, "text": str}'}

INSERT_DB_ERR = {'response': 'ERROR',
                 'massage': 'В процессе что-то пошло не так'}

INSERT_DB_SUCCESS = {'response': 'OK',
                     'massage': 'Объявление успешно создано'}

SELECT_DB_SUCCESS = {'response': 'OK', 'values': []}