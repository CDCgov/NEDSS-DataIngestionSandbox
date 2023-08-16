#
# Build stage
#
FROM amazoncorretto:17 as builder

#Copy project config
COPY gradle /usr/src/nbsauthenticator/gradle
COPY gradlew /usr/src/nbsauthenticator/gradlew
COPY gradle.properties /usr/src/nbsauthenticator/gradle.properties
COPY settings.gradle /usr/src/nbsauthenticator/settings.gradle
COPY build.gradle /usr/src/nbsauthenticator/build.gradle

#Copy sources
COPY . /usr/src/nbsauthenticator

WORKDIR /usr/src/nbsauthenticator

#Build jwtgenerator along with any required libraries
RUN ./gradlew -x test --no-daemon

FROM amazoncorretto:17

COPY --from=builder /usr/src/nbsauthenticator/build/libs/nbsauthenticator*.jar nbsauthenticator.jar

# Run jar
ENTRYPOINT ["java", "-jar", "nbsauthenticator.jar"]

