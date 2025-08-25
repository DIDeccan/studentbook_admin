# studentbook_admin
 
## TO DEVELOP USING DOCKER
 
### To build containers
#### $ docker compose build
 
### To run containers
#### $ docker compose up -d
 
### To view all containers logs
#### $ docker compose logs -f
 
### Single command to build, run and watch logs
#### $ docker compose up -d --build && docker compose logs -f
 
### To shut down containers
#### $ docker compose down
 
 
## TO DEVELOP WITHOUT DOCKER
 
### To run backend
#### 1) Activate virtual environment
#### 2) $ python manage.py runserver
 
### To run frontend
#### 1) node version ( 18.19.0 )
#### 2) $ npm install --legacy-peer-deps
#### 3) $ npm rebuild node-sass
#### 4) $ npm start