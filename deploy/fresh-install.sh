!#/bin/bash
sudo mkdir /home/crawler
sudo chmod 777 /home/crawler
cd /home/crawler/
sudo apt-get update && sudo apt-get -y upgrade
sudo apt-get install -y build-essential libxml2 libxslt1-dev python-dev python-pip git libjpeg-dev zlib1g-dev libpng12-dev
git clone https://github.com/gt-big-data/retina-crawler.git
cd retina-crawler
sudo pip install -r deploy/requirements.txt
sudo pip install PIL
nohup python main.py configs/prod-config.json &