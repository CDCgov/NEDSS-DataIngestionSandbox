# NBS - Gen 2 - Autenticator

To build loclly:
   gradle build

To run locally:
    java -cp "build/libs/nbsauthenticator-0.0.1-SNAPSHOT.jar" org.springframework.boot.loader.JarLauncher \
        --server.port=<specify_a_port_number> \
        --DI_NBS_DBSERVER=<get_value_from_config_map> \
        --DI_NBS_DBNAME=<get_value_from_config_map> \
        --DI_NBS_DBUSER=<get_value_from_config_map> \
        --DI_NBS_DBPASSWORD=<get_value_from_config_map> \
        --AUTH_FACTORY=<get_value_from_config_map> \
        --AUTH_SECRET=<get_value_from_config_map>

To build docker image locally: 
    docker build -t nbsauthenticator .
