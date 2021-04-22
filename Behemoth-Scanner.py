#/usr/bin/python

#from os import system
import subprocess
import sys
from os import system
from subprocess import Popen, PIPE
import socket



path_dir = "logs/"
system("rm -r "+path_dir+"output.log")
__subdomains = sys.argv[1]

def read_output_file():
	r_fl = open( path_dir + "output.log","r").readlines()
	for subdomain in r_fl:
		if "name = " in subdomain:
			sub = subdomain.split("name = ")
			sub = sub[1].strip()
			sub = sub[:-1]
			try:
				ip = socket.gethostbyname(sub)
			except:
				ip = "[Not Found]"
			print(sub+" - ["+ip+"]")

def write_output_file(content):
	fl = open( path_dir + "output.log", "a+")
	fl.write(content+"\n")
	fl.close()

def reverse_dnslookup(ip):
	process = Popen(['nslookup', ip], stdout=PIPE, stderr=PIPE)
	stdout, stderr = process.communicate()
	stdout = stdout.decode('utf-8')
	print(stdout)
	write_output_file(stdout)

def reverse_range(range_ip):
	for i in range(255):
		ip = str(range_ip)+"."+str(i)
		reverse_dnslookup(ip)

	read_output_file()

def save_ips(ip):
        fl = open(path_dir+"ips.log","a+")
        fl.write(ip+"\n")
        fl.close()



def read_content(ip):
	save_list = []
	file_header = open(path_dir+"ips.log","r").read()
	ip = ip.strip()
	if ip in file_header:
		pass
	else:
		#print "not have ip: "+ip
		save_ips(ip)
def check_range_ips(range_of_ips):
	for ip in range_of_ips:
		read_content(ip)
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

#check_range_ips(range_of_ips)
get_range_of_subs(__subdomains)

