class StatusCode:
    OK = {'code': 200}
    WARNING_NO_RECORD_FOUND = {'code': 300, 'desc': 'No Record found'}
    ERROR = {'code': 400, 'desc': 'General Error'}
    ERROR_DATABASE_CONNECTION = {'code': 401,
                                 'desc': 'Database connection error'}
    ERROR_INVALID_REQUEST = {'code': 402, 'desc': 'Invalid request'}
