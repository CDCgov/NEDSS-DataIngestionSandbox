# ./gradlew build && java -jar build/libs/kafka-connector-demo-0.0.1-SNAPSHOT.jar
# docker build --build-arg JAR_FILE=build/libs/\*.jar -t kafka-connector-demo .
FROM openjdk:17-oracle
ARG JAR_FILE=kafka-connector-demo/build/libs/*.jar
COPY ${JAR_FILE} app.jar
ENTRYPOINT ["java","-jar","/app.jar"]