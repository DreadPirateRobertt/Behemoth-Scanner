#/usr/bin/python

#from os import system
import subprocess
import sys
from os import system
from subprocess import Popen, PIPE
import socket
from alive_progress import alive_bar
import time


path_dir = "logs/"
__subdomains = sys.argv[1]

def read_output_file():
	#system("rm -r "+path_dir+"output.log")
	r_fl = open( path_dir + "output.log","r").readlines()
	for subdomain in r_fl:
		if "name = " in subdomain:
			sub = subdomain.split("name = ")
			sub = sub[1].strip()
			sub = sub[:-1]
			print(sub)
			read_and_remove_duplicates(path_dir+"subs-huntings-discovery.txt",sub)

def write_output_file(content):
	fl = open( path_dir + "output.log", "a+")
	fl.write(content+"\n")
	fl.close()

def reverse_dnslookup(ip):
	process = Popen(['nslookup', ip], stdout=PIPE, stderr=PIPE)
	stdout, stderr = process.communicate()
	stdout = stdout.decode('utf-8')
	#print(stdout)
	write_output_file(stdout)

def reverse_range(range_ip):

	def compute():
		for i in range(255):
			time.sleep(.01)  # process items
			yield
			ip = str(range_ip)+"."+str(i)
			reverse_dnslookup(ip)
		read_output_file()

	with alive_bar(255) as bar:
		for i in compute():
			bar()

	

def save_items(__file,item):
        fl = open(__file,"a+")
        fl.write(item+"\n")
        fl.close()



def read_and_remove_duplicates(__file,item):
	save_list = []
	file_header = open(__file,"r").read()
	item = item.strip()
	if item in file_header:
		pass
	else:
		#print "not have ip: "+ip
		save_items(__file,item)
def check_range_ips(range_of_ips):
	for ip in range_of_ips:
		read_and_remove_duplicates(path_dir+"ips.log",ip)
def get_range_of_subs(__subdomains):
	range_of_ips = []
	fl = open(__subdomains,"r").readlines()
	for sub in fl:
		try:
			sub_str = sub.strip()
			get_ip = socket.gethostbyname(sub_str)
			get_ip = str(get_ip)
			if get_ip[-2] == ".":
				print("[+] "+sub_str+" => "+get_ip+" ["+get_ip[:-2]+"]")
				if get_ip[:-2] in range_of_ips:
					continue
				else:
					range_of_ips.append(get_ip[:-2])
			elif get_ip[-3] == ".":
				print("[+] "+sub_str+" => "+get_ip+" ["+get_ip[:-3]+"]")
				if get_ip[:-3] in range_of_ips:
					continue
				else:
					range_of_ips.append(get_ip[:-3])
			elif get_ip[-4] == ".":
				print("[+] "+sub_str+" => "+get_ip+" ["+get_ip[:-4]+"]")
				if get_ip[:-4] in range_of_ips:
					continue
				else:
					range_of_ips.append(get_ip[:-4])
		except:
			pass
	check_range_ips(range_of_ips)

#get_range_of_subs(__subdomains)

fl = open("logs/ips.log","r").readlines()
for r in fl:
	reverse_range(r.strip())
	system("rm -r "+path_dir+"output.log")
