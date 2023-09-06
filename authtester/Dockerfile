#
# Build stage
#
FROM amazoncorretto:17 as builder

#Copy project config
COPY gradle /usr/src/authtester/gradle
COPY gradlew /usr/src/authtester/gradlew
COPY gradle.properties /usr/src/authtester/gradle.properties
COPY settings.gradle /usr/src/authtester/settings.gradle
COPY build.gradle /usr/src/authtester/build.gradle

#Copy sources
COPY . /usr/src/authtester

WORKDIR /usr/src/authtester

#Build software along with any required libraries
RUN ./gradlew -x test --no-daemon build

FROM amazoncorretto:17

COPY --from=builder /usr/src/authtester/build/libs/authtester-0.0.1-SNAPSHOT.jar authtester.jar

# Run jar
ENTRYPOINT ["java", "-jar", "authtester.jar"]

