Introduction
----
Garage will be initially developed to be used in Kuwait and into consideration plans to rollout to different GCC countries.

Fixture data
----
1. Users.json contains two users incase database is refreshed using ./manange resetdb (mo/aziz).
2. vehicle_database.tar.gz is a compressed data repository that contains all the models data. To load data into the database: ./manage load_model_lookup

Requirements
----
1. RabbitMQ Server - sudo apt-get install rabbitmq-server