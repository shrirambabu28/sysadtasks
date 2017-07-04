su -
groupadd admins
groupadd moderators
groupadd students

seq 0 | xargs -I %n sh -c "sudo useradd -m -d /home/user%n -G admins,moderators,students user%n"
seq 1 3 | xargs -I %n sh -c "sudo useradd -m -d /home/user%n -G moderators,students user%n"
seq 4 6 | xargs -I %n sh -c "sudo useradd -m -d /home/user%n -G students user%n"
seq 7 9 | xargs -I %n sh -c "sudo useradd -m -d /home/user%n user%n"

chgrp students /home/user{7..9}
chgrp moderators /home/user{4..6}
chgrp admins /home/user{1..3}

chmod 770 /home/user{0..9}

mkdir /home/user{0..9}/delta
mkdir /home/user{0..9}/delta/folder{1..10}

crontab -e
seq 0 9 | xargs -I %n sh -c ' cd /home/user%n/delta/ ;
seq 1 10 | xargs -I %m sh -c ' 21 15 * * 1-6 echo 'cat /dev/urandom |tr -dc a-zA-Z0-9 |fold -w 10 |head -n 1'> /home/user%n/delta/folder%m/file.txt ''
