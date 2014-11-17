import datetime, threading, time
from subprocess import call

next_call = time.time()

def foo():
  global next_call
  call(["python", "manage.py", "checkauction"])
  next_call = next_call+10
  threading.Timer( next_call - time.time(), foo ).start()

foo()
