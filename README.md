# installation guide 
1) find the correct printer ip and login on mainsail
2) go to machine page
3) push the refresh button on the update manager 
4) update all components 
5) login with putty or another ssh client 
6) clone the G1-Configs project 
    1. cd ~ 
    2. git clone https://github.com/gingeradditive/G1-Configs.git
    3. sudo sh ./G1-Configs/install.sh 2>&1 | tee output.txt