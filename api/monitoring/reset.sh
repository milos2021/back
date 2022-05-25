echo "[]" > data_prod.json
echo "[]" > data_betradar.json
echo "{}" > data.json
echo "{}" > data_razrada.json
echo "{}" > data_all.json
echo "{}" > aktuelni.json
echo "[]" > razrada_mini.json
echo "[]" > data_nepovezani.json
echo "{}" > asian_prepared.json
echo '{"is_process_running":0}' > process_running.json 
sudo service cron stop
sudo service gunicorn stop
sudo rm versions.txt
sudo touch versions.txt
sudo chmod 777 versions.txt
find  . -name 'razlika_*' -exec rm {} \;
/home/milos/reporting/api/soccerenv/bin/python3 lista_base.py
find  . -name 'razlika_*' -exec rm {} \;
sudo rm versions.txt
sudo touch versions.txt
sudo chmod 777 versions.txt
echo '{"is_process_running":0}' > process_running.json 
sudo service cron start
sudo service gunicorn start
