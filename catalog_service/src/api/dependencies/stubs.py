from typing import NoReturn


def get_config() -> NoReturn:
    raise NotImplementedError()


def get_redis_gateway() -> NoReturn:
    raise NotImplementedError()


def get_elasticsearch_gateway() -> NoReturn:
    raise NotImplementedError()
