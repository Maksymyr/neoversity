# Скопіюйте цей файл у configs.py і впишіть параметри підключення до Kafka.
# configs.py не потрапляє в git, див. .gitignore.
kafka_config = {
    "bootstrap_servers": ["<host>:9092"],
    "username": "<username>",
    "password": "<password>",
    "security_protocol": "SASL_PLAINTEXT",
    "sasl_mechanism": "PLAIN",
}
