import os

IST_IMAGE_STORAGE_FOLDER = os.environ.get('IST_IMAGE_STORAGE_FOLDER', "./server/storage")

IST_SERVICE_HOST = os.environ.get('IST_SERVICE_HOST', '127.0.0.1')
IST_SERVICE_PORT = os.environ.get('IST_SERVICE_PORT', 9999)

# Should be removed from source code. Only for local testing now
IST_DB_USER = os.environ.get('IST_DB_USER', 'postgres')
IST_DB_PASSWORD = os.environ.get('IST_DB_PASSWORD', '123456789test_user')
IST_DB_HOST = os.environ.get('IST_DB_HOST', 'db')
IST_DB_PORT = os.environ.get('IST_DB_PORT', 8888)
