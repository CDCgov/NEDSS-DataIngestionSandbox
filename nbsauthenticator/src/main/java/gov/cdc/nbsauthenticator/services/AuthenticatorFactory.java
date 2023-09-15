package gov.cdc.nbsauthenticator.services;

import 	lombok.NoArgsConstructor;
import 	org.springframework.stereotype.Service;
import 	org.springframework.beans.factory.annotation.Value;
import  org.springframework.beans.factory.annotation.Autowired;

import  org.slf4j.Logger;
import  org.slf4j.LoggerFactory;

@Service
@NoArgsConstructor
public class AuthenticatorFactory {
    private static Logger logger = LoggerFactory.getLogger(AuthenticatorFactory.class);

    private static String NBSCLASSIC_PROVIDER = "nbsclassic";
    private static String OKTA_PROVIDER = "okta";
    private static String KEYCLOCK_PROVIDER = "keycloak";

    @Value("${auth.provider}")
    private String authProvider;

    @Autowired
    private IAuthenticator keyCloakAuthAuthenticator;

    @Autowired
    private IAuthenticator oktaAuthAuthenticator;

    @Autowired
    private IAuthenticator nbsClassicAuthAuthenticator;

    public IAuthenticator getAuthenticator() {
        IAuthenticator authenticator = nbsClassicAuthAuthenticator; // default

        logger.info("Authentication provider = {}", authProvider);

        if( OKTA_PROVIDER.equals(authProvider) ) {
            authenticator = oktaAuthAuthenticator;
        }
        else if( KEYCLOCK_PROVIDER.equals(authProvider) ) {
            authenticator = keyCloakAuthAuthenticator;
        }

        return authenticator;
    }
}
