class Command(object):
    # Permission level for this command
    LOCAL = 100
    GUEST = 10
    SERVER = 50
    JN_XYP = 1024

    cmd_ref = ''
    execute = None  # type:function
    level = None  # type: int

    def __init__(self, cmd_ref: str, execute, level: int):
        self.cmd_ref = cmd_ref
        self.execute = execute
        self.level = level


class Assigned_Function_Error(ValueError):
    msg = ''

    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self) -> str:
        return self.msg


def a(b:int, c:int):
    pass

cmd = Command('a', a, 0)
