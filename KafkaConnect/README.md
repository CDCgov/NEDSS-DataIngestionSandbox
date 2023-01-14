# Installation guide
Requirement:
- Docker version 1.11 or later
- Java version 17
- Mongo (local setup for testing)
- Postgres (local setup for testing)

Installation:
- Go to  kafka directory and run docker-compose up -d
    - kafka docker container should be executed and runninng.
- Setup connector
    - connector should be available in port 8083
    - execute the following endpoint to create connect config
    - POST: localhost:8083/connectors
        - payload:
            ```
            {
                "name":"mongo-source-connector-dlq-test",
                "config": {
                    "connector.class":"com.mongodb.kafka.connect.MongoSourceConnector",
                    "tasks.max":1,
                    "connection.uri":"mongodb://gateway.docker.internal:27017",
                    "database":"test",
                    "collection":"data",
                    "poll.max.batch.size":"1000",
                    "poll.await.time.ms":"5000",
                    "batch.size":0,
                    "change.stream.full.document":"updateLookup"
                }
            }
            ```
    - check newly created config
    - GET: localhost:8083/connectors
    - Result: the endpoint should return all existing connector
    
- Setup test project
    - Assuming you already have both Mongo and Posgres installed and running on default port
        - After Mongo is installed, go to mongod.conf and add replication add follow:
            ```
            systemLog:
              destination: file
              path: /opt/homebrew/var/log/mongodb/mongo.log
              logAppend: true
            storage:
              dbPath: /opt/homebrew/var/mongodb
            net:
              bindIp: 127.0.0.1,::1
              ipv6: true
            replication:
              replSetName: "replica0"
            ```
    - There are two test project producer (kafka-connector-demo) and consumer (kafka-consumer-demo)
        - Kafka-connector-demo is a REST service where you can insert test data into mongo and trigger Kafka process.
        - Kafka-consumer-demo (DEPRECATED) is a microservice where it automatically pick up the data that was triggered by the REST service. 
        - Spring-consumer-demo, same old consumer but utilize Spring also support retry and dlq workflow
    - For the sake simplicity, these two services can be executed on IntelliJ 