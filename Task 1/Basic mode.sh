for i in $(seq 0 9);
do
	useradd user$i	
	mkdir /home/user$i/delta	
	for j in $(seq 1 10);
	do
		mkdir /home/user$i/delta/folder$j
		echo `cat /dev/random | tr -dc 'a-zA-Z0-9' | fold -w 10 | head -n 1` > /home/user$i/delta/folder$j/random.txt
	done
done
groupadd admins
groupadd moderators
groupadd students

for i in $(seq 1 9);
do
        setfacl -R -m u:user0:rwx /home/user$i/delta
done
for i in $(seq 1 3);
do
	usermod -a -G admins user$i
	setfacl -R -m u:user0:rwx /home/user$i/delta
done
for i in $(seq 4 6);
do
	usermod -a -G moderators user$i
	setfacl -R -m g:admins:rwx /home/user$i/delta
done
for i in $(seq 7 9);
do
	usermod -a -G students user$i
	setfacl -R -m g:admins:rwx /home/user$i/delta
	setfacl -R -m g:moderators:rwx /home/user$i/delta
done
