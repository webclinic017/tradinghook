from app.common_db import is_present 

if is_present("users"):
  print("yes")
else:
  print("no")