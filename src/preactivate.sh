apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 0C49F3730359A14518585931BC711F9BA15703C6
echo "deb [ arch=amd64,arm64 ] http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.4.list
apt-get update
apt-get install -y mongodb-org virtualenv python-pip

virtualenv env
env/bin/pip install flask
env/bin/pip install mongokit
env/bin/pip install nba_py
env/bin/pip install -I pymongo==2.8
