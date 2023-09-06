package gov.cdc.nbsauthenticator.services;

import  gov.cdc.nbsauthenticator.services.authimpls.OktaAuthAuthenticator;
import  gov.cdc.nbsauthenticator.services.authimpls.NbsClassicAuthAuthenticator;
import  gov.cdc.nbsauthenticator.services.TokenGenerator;
import  gov.cdc.nbsauthenticator.repositories.NbsAuthUsersRepository;
import  gov.cdc.nbsauthenticator.repositories.NbsAuthUserRolesRepository;

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

    @Value("${auth.provider}")
    private String authProvider;

    @Autowired
    private NbsAuthUsersRepository authUsersRepository;

    @Autowired
    private NbsAuthUserRolesRepository authRolesRepository;

    @Autowired
    private TokenGenerator tokenGenerator;

    public IAuthenticator getAuthenticator() {
        IAuthenticator authenticator = (OKTA_PROVIDER.equals(authProvider)
                                            ? new OktaAuthAuthenticator()
                                            : new NbsClassicAuthAuthenticator());

        authenticator.setAuthUserRepository(authUsersRepository);
        authenticator.setAuthRolesRepository(authRolesRepository);
        authenticator.setTokenGenerator(tokenGenerator);

        return authenticator;
    }
}
