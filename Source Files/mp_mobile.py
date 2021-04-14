import re
import os
import sys
import atexit
import argparse
import subprocess

try:
    import urllib3
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'urllib3'])
finally:
    import urllib3
try:
	import progressbar
except ImportError:
	subprocess.check_call([sys.executable,"-m","pip","install","progressbar2"])
finally:
	import progressbar
try:
	from colorama import Fore, Style, init
except ImportError:
	subprocess.check_call([sys.executable,"-m","pip","install","colorama"])
finally:
	from colorama import Fore, Style, init

class MissingArgumentError(Exception):
	def __init__(self,arg):
		self.arg = arg
		self.message = "Missing argument:"
		super().__init__(self.message)
	def __str__(self):
		return f"{self.message}: {self.arg}"
		
def download(link : str, maximum : int = None,path : str = None, debug : bool = False) -> None:
	broken = False
	if path is None:
		path = "/storage/emulated/0/download/"
	if debug:
		print(Fore.BLUE+"Base path: {}".format(path))
	pool = urllib3.PoolManager()
	response = pool.request("GET",link)
	data = response.data.decode("utf-8")
	arr = re.findall(r'(?<={}).*?(?={})'.format("<p class=\"jb-image\"><img src=\"","\" alt=\"\" /><br/></p>"), data)
	for i in arr:
	           if "?itok=" in i:
	           	broken = True
	if broken == True:
		arr = re.findall(r'(?<={}).*?(?={})'.format("<p class=\"jb-image\"><img src=\"","\?itok="), data)
	title = link.split("/")[-1]
	if maximum is None:
		maximum = len(arr)
	arr = arr[:int(maximum)]
	if debug:
		print(Fore.LIGHTWHITE_EX+"Links are: {}".format(arr))
	directory = os.path.join(path, title)
	if debug:
		print(Fore.BLUE+"Attempting to save to: {}".format(directory))
	count = 0
	while True:
	           if not os.path.exists(directory):
	           	os.makedirs(directory)
	           	break
        	   else:
            		count += 1
            		directory = os.path.join(path, title+"_"+str(count))
	path = directory
	if debug:
		print(Fore.BLUE+"Saving to: {}".format(path))
	count = 1
	for url in progressbar.progressbar(arr):
		response = pool.request("GET",url).data
		try:
			response.decode("utf-8")
			if debug:
				print(Fore.RED+"Missing imge: {}".format(count))
			continue
		except UnicodeDecodeError:
			if debug:
				print(Fore.GREEN+"Image found: {}".format(count))
		with open(path+"/"+title+"_"+str(count)+".png","wb") as file:
			file.write(response)
		print(Style.RESET_ALL)
		count += 1
	print("Success")
	ending = None
	while ending != "":
		ending = input(Fore.GREEN+"Press ENTER to exit\n"+Style.RESET_ALL)

init()

def destructor():
	print(Style.RESET_ALL)
	
atexit.register(destructor)		
parser = argparse. ArgumentParser(description="Download comics")

parser.add_argument("Url",metavar="url",type=str,help="Comic url")
parser.add_argument("-m","--max",action="store",help="Maximum images")
parser.add_argument("-p","--path",action="store",help="Custom download path")
parser.add_argument("-D","--DEBUG",action="store_true",help="Debug flag")

args = parser.parse_args()

if args.Url is not None:
	download(args.Url,args.max,args.path,args.DEBUG)
else:
	raise MissingArgumentError("Url")
