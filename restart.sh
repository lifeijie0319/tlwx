#ps -ef|grep main.py|grep -v grep|awk '{print $2}'|xargs kill -9
#ps -ef|grep xmlserver|grep -v grep|awk '{print $2}'|xargs kill -9
nohup python xmlserver.py --logging=debug >> log/xmlserver.log &
nohup python main.py --logging=debug >> log/main.log &
