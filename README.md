# Stock Bot
Backend written in Flask for a stock bot to track gym equipment. 
Performs scraping of supported items on a scheduled basis (~5 minutes) via Celery.

## Currently supported manufacturers:
- Rogue
- ATX

## Structure
1. Flask (backend) 
2. MongoDB (db)
3. Redis (broker)
4. Celery (worker)