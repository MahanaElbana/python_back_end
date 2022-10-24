import re

password = "@@@@@aAr0opopopopop"
if re.findall(r"^.*(?=.{16,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).*$", password):
   print("true")
else:
    print("false")