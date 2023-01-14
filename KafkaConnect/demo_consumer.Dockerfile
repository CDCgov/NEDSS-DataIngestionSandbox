#./gradlew build && java -jar build/libs/spring-comsumer-demo-0.0.1-SNAPSHOT.jar

#docker build --build-arg JAR_FILE=build/libs/\*.jar -t ndduc/spring-comsumer-demo .

FROM openjdk:17-oracle
ARG JAR_FILE=spring-comsumer-demo/build/libs/*.jar
COPY ${JAR_FILE} app.jar
ENTRYPOINT ["java","-jar","/app.jar"]