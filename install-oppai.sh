mkdir tmp
cd tmp
wget https://github.com/Francesco149/oppai-ng/archive/HEAD.tar.gz
tar xf HEAD.tar.gz
cd oppai-*
./build
sudo install -Dm 755 oppai /usr/bin/oppai
cd ..
cd ..
rm -rf tmp
oppai