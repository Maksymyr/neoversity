# Скопіюйте у configs.py і впишіть дані для підключення. configs.py не потрапляє в git.
kafka_config = {
    "bootstrap_servers": ["<host>:9092"],
    "username": "<username>",
    "password": "<password>",
    "security_protocol": "SASL_PLAINTEXT",
    "sasl_mechanism": "PLAIN",
}

mysql_config = {
    "host": "<host>",
    "port": 3306,
    "user": "<username>",
    "password": "<password>",
}
