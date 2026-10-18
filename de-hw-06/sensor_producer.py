import argparse
import random
import time

from kafka import KafkaProducer

from kafka_common import BUILDING_SENSORS_TOPIC, connection_params, now_iso, serialize

TEMPERATURE_RANGE = (25.0, 45.0)
HUMIDITY_RANGE = (15.0, 85.0)

# макс зміна за один крок
TEMPERATURE_STEP = 1.0
HUMIDITY_STEP = 3.0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Імітація одного датчика температури та вологості")
    parser.add_argument("--interval", type=float, default=2.0, help="пауза між вимірами в секундах")
    parser.add_argument("--count", type=int, default=0, help="кількість вимірів, 0 означає працювати до Ctrl+C")
    return parser.parse_args()


def next_value(current: float, step: float, bounds: tuple[float, float]) -> float:
    # якщо вийшли за межу, відбиваємось назад, щоб значення не залипало на краю
    low, high = bounds
    value = current + random.uniform(-step, step)
    if value > high:
        value = 2 * high - value
    elif value < low:
        value = 2 * low - value
    return value


def main() -> None:
    args = parse_args()

    # один запуск = один датчик
    sensor_id = random.randint(1000, 9999)

    temperature = random.uniform(*TEMPERATURE_RANGE)
    humidity = random.uniform(*HUMIDITY_RANGE)

    producer = KafkaProducer(
        **connection_params(),
        key_serializer=serialize,
        value_serializer=serialize,
    )

    print(f"Sensor {sensor_id} started, sending to '{BUILDING_SENSORS_TOPIC}'")
    sent = 0
    try:
        while args.count == 0 or sent < args.count:
            temperature = next_value(temperature, TEMPERATURE_STEP, TEMPERATURE_RANGE)
            humidity = next_value(humidity, HUMIDITY_STEP, HUMIDITY_RANGE)
            reading = {
                "id": sensor_id,
                "temperature": round(temperature, 1),
                "humidity": round(humidity, 1),
                "timestamp": now_iso(),
            }
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
