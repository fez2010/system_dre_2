#!/bin/bash
echo "ttf-mscorefonts-installer msttcorefonts-eula select true" | sudo debconf-set-selections
sudo apt-get install msttcorefonts ttf-mscorefonts-installer -y --reinstall
sudo fc-cache -f
fc-match "Arial"