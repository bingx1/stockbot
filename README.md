# Stock Bot
Simple web application to track the stock status of gym equipment. 
Built to simplify the experience of building a home gym in 2020-2021.
Developed in response to the shortage brought upon by COVID-19 and the unreliability of manufacturers' own email restock alerts.
Items are automatically refreshed in the background every 5 minutes through Celery.
 
## Author
Bing Xu
![alt_text](https://user-images.githubusercontent.com/50439413/113514032-bb5a3a00-95af-11eb-8b17-7b29446a546a.png)
![alt text](https://user-images.githubusercontent.com/50439413/113513829-d8423d80-95ae-11eb-8ddb-c207a86ad4c6.png)



### Currently supported manufacturers and websites:
- Rogue
- Samsfitness (ATX, Ironmaster)
- Kabuki Strength

## Changelog
v.1.0: Beta
- Serving simple bootstrap frontend
- Supports items from roguefitness.com, samsfitness.com.au and store.kabukistrength.net
- Celery background refreshing is working as intended
- App must be run in separate terminals .... not yet containerized


# TODO
1. Dockerize the backend
2. Implemenet exception handling for scraping/refreshing of stock status
3. Containerize entire application (write a docker-compose)
4. Move front-end to react

## Quickstart
- Clone this repository and install docker.
- Run redis and mongodb in a container (or locally)
- Start the flask backend
- Run the celery workers and celery beat scheduler
- Visit http://127.0.0.1:5000/ to see the app running!

## Project Structure
1. Flask (backend) 
2. MongoDB (db)
3. Redis (broker)
4. Celery (worker)



