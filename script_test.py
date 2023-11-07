#!./.venv/bin/python
from lib.janus import janus
import scripts

bot = janus('calibration.ini', test=True)
scripts.security_mode_infinite(bot)
