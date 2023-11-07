# start up service
docker compose up -d;

# ssh into database
osascript -e 'tell app "Terminal" 
    do script "docker exec -it db /bin/bash" 
end tell';