from typing import Collection, Union


def _get_arg_positions(func):
    return {arg: pos for pos, arg in enumerate(func.__annotations__)}


def assert_in_collection(collections: Collection[Collection], arguments: Collection, is_class_method=True):
    assert len(collections) == len(arguments), f'Mismatch length of collections {len(collections)} and arguments {len(arguments)}'

    def decorator(func):
        arg_positions = _get_arg_positions(func)
        func_anns = func.__annotations__

        def wrapper(*args, **kwargs):
            for collection, argument in zip(collections, arguments):
                value = kwargs.get(argument)

                value = value if value is not None else args[arg_positions[argument] + int(is_class_method)]
                try:
                    assert value in collection
                except AssertionError:
                    if isinstance(value, str):
                        value = value.lower()
                assert value in collection, f'Value of the argument "{argument}" must be in {collection}, was passed {value}'
            return func(*args, **kwargs)

        wrapper.__annotations__ = func_anns
        return wrapper

    return decorator


def assert_not_None(arguments: Union[Collection, str]):
    if isinstance(arguments, str):
        arguments = (arguments)

    def decorator(func):

        arg_positions = _get_arg_positions(func)
        func_anns = func.__annotations__

        def wrapper(*args, **kwargs):
            for argument in arguments:
                value = kwargs.get(argument)
                if value:
                    assert value is not None, f'Argument "{argument}" must not be None'
                else:
                    assert args[arg_positions[argument]] is not None, f'Argument "{argument}" must not be None'
            return func(*args, **kwargs)

        wrapper.__annotations__ = func_anns
        return wrapper

    return decorator
