# zibal
This project is simple project have 2 api for show transaction 

 1)first api live query on DB and calculate

 2)second api use cache data 
 
For this projects and connect to DB used djongo(Python Object to MongoDB Document and Relational Database Mapper) that we can use django ORM and for professional and Complicated queries used pymongo like (aggregate and group by queries)

## REST FRAMEWORK
This projects develop in DRF and if we want use mongodb engine it not support drf.

The style guide used is PEP8. 

### cache command 
python manage.py cache_command

command for cache and save data on new collection (transactioncache) 
