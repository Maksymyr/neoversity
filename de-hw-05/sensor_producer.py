import argparse
import random
import time

from kafka import KafkaProducer

from kafka_common import BUILDING_SENSORS_TOPIC, connection_params, now_iso, serialize

TEMPERATURE_RANGE = (25, 45)
HUMIDITY_RANGE = (15, 85)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Імітація одного датчика температури та вологості")
    parser.add_argument("--interval", type=float, default=2.0, help="пауза між вимірами в секундах")
    parser.add_argument("--count", type=int, default=0, help="кількість вимірів, 0 означає працювати до Ctrl+C")
    return parser.parse_args()


def read_sensor(sensor_id: int) -> dict:
    return {
        "sensor_id": sensor_id,
        "timestamp": now_iso(),
        "temperature": round(random.uniform(*TEMPERATURE_RANGE), 1),
        "humidity": round(random.uniform(*HUMIDITY_RANGE), 1),
    }


def main() -> None:
    args = parse_args()

    # Один запуск скрипту імітує один датчик зі сталим випадковим ID
    sensor_id = random.randint(1000, 9999)

    # Ключ повідомлення це ID датчика, тому всі виміри одного датчика потрапляють
    # в одну партицію й читаються в порядку запису
    producer = KafkaProducer(
        **connection_params(),
        key_serializer=serialize,
        value_serializer=serialize,
    )

    print(f"Sensor {sensor_id} started, sending to '{BUILDING_SENSORS_TOPIC}'")
    sent = 0
    try:
        while args.count == 0 or sent < args.count:
            reading = read_sensor(sensor_id)
            # .get() чекає підтвердження брокера, тому помилку відправки буде видно одразу
            metadata = producer.send(BUILDING_SENSORS_TOPIC, key=sensor_id, value=reading).get(timeout=10)
            sent += 1
            print(
                f"[{reading['timestamp']}] sensor {sensor_id}: "
                f"t={reading['temperature']:.1f}°C h={reading['humidity']:.1f}% "
                f"-> partition {metadata.partition}, offset {metadata.offset}"
            )
            time.sleep(args.interval)
    except KeyboardInterrupt:
        pass
    finally:
        producer.close()
        print(f"Sensor {sensor_id} stopped, {sent} readings sent")


if __name__ == "__main__":
    main()
