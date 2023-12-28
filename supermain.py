import os
import db



# import main

confs = db.conf()

print("starting up")
for conf in confs:
	print(f"i : {conf}")
	cmd = "python main.py"
	for i in conf:
		cmd += f" {i}"
	os.system(cmd)

