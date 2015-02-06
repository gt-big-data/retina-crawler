!#/bin/sh

HOME=/home/crawler

# Create the crawler user.
# Specifically, we only care about the home directory.
sudo useradd -d $HOME crawler
sudo apt-get update && sudo apt-get -y upgrade
sudo apt-get install -y build-essential libxml2 libxslt1-dev python-dev python-pip git libjpeg-dev zlib1g-dev libpng12-dev
git clone https://github.com/gt-big-data/retina-crawler.git
cd $HOME
cd retina-crawler/
sudo pip install -r deploy/requirements.txt
deploy/run.sh
