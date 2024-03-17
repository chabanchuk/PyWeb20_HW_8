from models import Author, Quote
from enum import Enum
import redis
from redis_lru import RedisLRU

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


class Command(Enum):
    NAME = "name"
    TAGS = "tag"
    EXIT = "exit"

@cache
def find_by_tag(tag: str) -> list[str | None]:
    print(f"Find by {tag}")
    quotes = Quote.objects(tags__iregex=tag)
    result = [q.quote for q in quotes]
    return result

@cache
def find_by_author(author: str) -> list:
    print(f"Find by {author}")
    authors = Author.objects(fullname__iregex=author)
    result = {}
    for a in authors:
        quotes = Quote.objects(author=a)
        result[a.fullname] = [q.quote for q in quotes]
    return result

def process_command():
    while True:
        user_input = input("Enter command: ")
        if user_input.strip() == Command.EXIT.value:
            return
        if ':' in user_input:
            command, value = user_input.split(':', 1)
            value = value.strip()
        else:
            command = user_input.strip()
            value = ''
        command = command.strip()
        match command:
            case Command.NAME.value:
                print(find_by_author(f".*{value}.*"))
            case Command.TAGS.value:
                print(find_by_tag(f".*{value}.*"))
            case Command.EXIT.value:
                return
            case _:
                print("Unknown command")

if __name__ == '__main__':
    process_command()
