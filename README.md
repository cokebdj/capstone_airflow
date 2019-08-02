# capstone_airflow

docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)


docker run -v /home/ubuntu/Desktop/capstone_airflow:/usr/local/airflow -v /home/ubuntu/Desktop/capstone_airflow/requirements.txt:/requirements.txt -p 8080:8080 puckel/docker-airflow webserver

