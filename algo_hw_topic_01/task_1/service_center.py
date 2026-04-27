import random
from dataclasses import dataclass, field
from datetime import datetime
from itertools import count
from queue import Queue

from colorama import Fore, init

init(autoreset=True)

REQUEST_TYPES = ("installation", "repair", "consultation", "diagnostics", "warranty")
_id_counter = count(1)


@dataclass
class Request:
    id: int = field(default_factory=lambda: next(_id_counter))
    kind: str = field(default_factory=lambda: random.choice(REQUEST_TYPES))
    created_at: datetime = field(default_factory=datetime.now)

    def __str__(self) -> str:
        return f"#{self.id:04d} [{self.kind}] @ {self.created_at:%H:%M:%S}"


def generate_request(queue: Queue) -> Request:
    request = Request()
    queue.put(request)
    print(f"{Fore.CYAN}+ new request:    {request}")
    return request


def process_request(queue: Queue) -> Request | None:
    if queue.empty():
        print(f"{Fore.YELLOW}! queue is empty — nothing to process")
        return None

    request = queue.get()
    print(f"{Fore.GREEN}- processed:      {request}")
    return request


def print_status(queue: Queue) -> None:
    print(f"{Fore.MAGENTA}= queue size:     {queue.qsize()}")


MENU = (
    "g — generate new request",
    "p — process next request",
    "s — show queue status",
    "a — auto: generate & process random number of requests",
    "q — quit",
)


def main() -> None:
    queue: Queue = Queue()
    print(f"{Fore.MAGENTA}Service center simulator")
    for line in MENU:
        print(f"  {line}")

    while True:
        choice = input(f"{Fore.GREEN}> ").strip().lower()

        if choice in ("q", "quit", "exit"):
            print(f"{Fore.MAGENTA}Shutting down. Unprocessed requests: {queue.qsize()}")
            break
        elif choice == "g":
            generate_request(queue)
        elif choice == "p":
            process_request(queue)
        elif choice == "s":
            print_status(queue)
        elif choice == "a":
            for _ in range(random.randint(1, 5)):
                generate_request(queue)
            for _ in range(random.randint(1, 5)):
                process_request(queue)
            print_status(queue)
        else:
            print(f"{Fore.RED}Unknown command. Use one of: g, p, s, a, q")


if __name__ == "__main__":
    main()
