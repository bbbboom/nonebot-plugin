from nonebot.default_config import *

DEBUG = False
SUPERUSERS = {}
COMMAND_START = {'', '/', '!', '#'}
SESSION_EXPIRE_TIMEOUT = timedelta(seconds=120)
SESSION_RUN_TIMEOUT = timedelta(seconds=60)
MAX_VALIDATION_FAILURES = 3
TOO_MANY_VALIDATION_FAILURES_EXPRESSION = '你输入错误次数太多啦！'
SESSION_RUNNING_EXPRESSION = 'waiting'
