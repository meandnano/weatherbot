from typing import TypeVar, Optional

VAR = TypeVar("VAR")


class VarNotProvidedException(Exception):
    env_var: str

    def __init__(self, env_var: str):
        self.env_var = env_var

    def __str__(self):
        return f"Env var {self.env_var} is not provided. Could also be served trough .env file"


def require_env(var: Optional[VAR], var_name: str) -> VAR:
    if var is None:
        raise VarNotProvidedException(var_name)

    return var
