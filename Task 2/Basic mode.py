#A tool to synchronize two directories with the help of rolling checksum(adler-32) and md5 hash!
#!/usr/bin/python
import os
import hashlib
import shutil
import fractions
import zlib
import sys
from zlib import adler32

BLOCKSIZE=2**n
for fname in sys.argv[1:]:
 asum = 1
 with open(fname) as f:
   while True:
     data = f.read(BLOCKSIZE)
     if not data:
    	break
     asum = adler32(data, asum)
     if asum < 0:
       asum += 2**32

 print hex(asum)[2:10].zfill(8).lower(), fname


print "Enter the paths of the two directories you'd like to sync."

dir1 = sys.argv[1] 
dir2 = sys.argv[2]

if dir1[-1] != '/':
	dir1 += '/'
if dir2[-1] != '/':
	dir2 += '/'
if not os.path.exists(dir1) and not os.path.exists(dir2):
	print("Error: arguments are not directories")
elif os.path.exists(dir1) or os.path.exists(dir2):
	# make directory
	if not os.path.isdir(dir1):
		os.makedirs(dir1)
	elif not os.path.isdir(dir2):
		os.makedirs(dir2)
maxbar=input("Enter maximum bar for the size of the file in bytes.")
maxbar!=-1

for filename in os.listdir(dir1):
	dir1path = dir1 + "/" + filename
	dir1stat = os.stat(dir1path)
		
	if ((dir1stat.st_size <= maxbar) or (maxbar == -1)):
		
		dir2path = dir2 + "/" + filename
		
		if (not os.path.exists(dir2path)):
			shutil.copy2(dir1path, dir2path)
			continue
			
		dir1stat = os.stat(dir1path)
		dir2stat = os.stat(dir2path)

		dir1orisize = dir1stat.st_size
		dir1size = dir1stat.st_size
		dir2size = dir2stat.st_size

                if ([dir1size, int(dir1stat.st_mtime)] != [dir2size, int(dir2stat.st_mtime)]):
					
			if ((dir1size) <= 32 or (dir2size <= 32)):
				shutil.copy2(dir1path, dir2path)
				continue

			sms = min(dir1size, dir2size)
				
			n = 5
			while True:
				bs = 2**n
				if (bs > (sms/500)):
					break
				if (bs == 524288):
					break
				n += 1

			rfcs = []
			rfmd5 = []
			rf = open(dir2path, "rb+")

			ts = 0
			while True:
				ts += bs
				if (ts >= dir2size):
					rfts = ts
					break

			rf.truncate(rfts)
			dir2size = os.stat(dir2path).st_size

			while True:
				if (rf.tell() == dir2size):
					break
				data = receiver_file.read(block_size)
				dcs = zlib.adler32(data)
				dmd5 = hashlib.md5(data).hexdigest()
				rfcs += [dcs]
				rfmd5 += [dmd5]

			rf.close()

			sf = open(dir1path, "rb+")

			ts = 0
			while True:
				ts += bs
				if (ts >= dir1size):
					sfts = ts
					break

			sf.truncate(sfts)
			dir1size = os.stat(dir1path).st_size

			dot_pos = dir1path.find(".")
			ntf = open(dir2+"/"+"ntf"+dir1path[dot_pos::], "wb+")
				
			while True:
				if (sf.tell() == dir1size):
					break
				if ((dir1size - sf.tell()) <= bs):
					data = sf.read(bs)
					ntf.write(data.rstrip("\n\00"))
					break
				data = sf.read(bs)
				dcs = zlib.adler32(data)
				dmd5 = hashlib.md5(data).hexdigest()
				if (dcs in rfcs):
					if (dmd5 in rfmd5):
						ntf.write(data)
						continue
				print data
				ntf.write(data[:1:])
				sf.seek(-(bs-1), 1)

			ntf.close()

			os.remove(dir2path)
			os.rename(dir2+"/"+"ntf"+dir1path[len(dir1path)-4::], dir2path)

			sf.truncate(dir1orisize)
                            
                os.remove(dir1path)

print "dir1 and dir2 are synchronised!"
