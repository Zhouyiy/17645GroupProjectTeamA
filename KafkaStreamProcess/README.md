# Kafka Stream Data Query, Process, and Store
## Introduction
This java project is aimed to read data from Kafka topic, re-structure the data and store the data into certain kind of datastore (maybe NoSQL database in the future, in current stage we choose to store them into json files). <br>
The basic idea is to create a KafkaConsumer to subscribe to Kafka topic and receive the data from this topic (movielog). Then extract the most useful parameters like "user id" and "movie id" and contruct them into data model objects. 

## Data Type Discussiong
### Raw data read from Kafka topic
We can get a series ConsumerRecord after polling from the topic by consumer. For each record, the important data information is stored in record.value(). We found there are two types of record value here:
1. WatchData
  - Description: This data is used to represent the information of a user watch a movie.
  - Example: 2019-09-05T19:27:01,614,GET /data/m/brides+2004/20.mpg
  - Data field :
    - Timestamp
    - user_id
    - movie_id
    - chunk_number
      - /data/m/{movie name separated by +}+{year}/{chunk_number}.mpg
    - media type
2. RateData
   - Description: This data is used to represent the information of how a user rate a movie
   - Example: 2019-09-05T19:27:01,118106,GET /rate/grumpier+old+men+1995=3
   - Data field :
      - Timestamp
      - user_id
      - movie_id
      - rate
            - /rate/{movie name separated by +}+{year}={rate}
    
Notice that in "{movie name separated by +}+{year}", it is possible that the year information is missing, which would result into "{movie name separated by +}+" (end with +). 

## Gradle \ Lombok Notes 
### Gradle
This program is managed by Gradle, here are several notes when compiling or running the program.
* Do "gradle build" to compile / recompile the program
* Do "gradle run --args='1000'" to run the program with a specified parameter 1000. (Here, the parameter 1000 means the number of data we want to read from Kafka, you can changed it to any positive number which is less than Integer.MAX_VALUE.)

### Project Lombok
This program uses Project Lombok as the annotation processor. If you are using Intellij as IDE, you need to go to 
"Settings > Build > Compiler > Annotation Processors”
to enable the Lombok to process the annotation like @Data, and @RequiredArgsConstructor. 

## Development Environment
* JDK version: 11
* Build Tool: Gradle (https://gradle.org/)
* Automatic Annotation Management: Project Lombok (https://projectlombok.org/)
* Testing / Debugging tools: JUnit, checkstyle, jacocoTest, spotBugs