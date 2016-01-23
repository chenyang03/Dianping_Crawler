mkdir Data
mkdir Data/Shops
echo "1" > status.txt
sudo apt-get update -y
sudo apt-get install python-pip firefox xvfb openssh-server -y
sudo pip install selenium
