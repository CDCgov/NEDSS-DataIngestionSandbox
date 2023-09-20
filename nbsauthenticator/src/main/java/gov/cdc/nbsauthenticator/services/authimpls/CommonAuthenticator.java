package gov.cdc.nbsauthenticator.services.authimpls;

import  gov.cdc.nbsauthenticator.services.IAuthenticator;
import  gov.cdc.nbsauthenticator.repositories.NbsAuthUsersRepository;
import  gov.cdc.nbsauthenticator.repositories.NbsAuthUserRolesRepository;
import  gov.cdc.nbsauthenticator.services.ITokenGenerator;

import	lombok.NoArgsConstructor;
import	lombok.Getter;
import	lombok.Setter;

import  org.slf4j.Logger;
import  org.slf4j.LoggerFactory;

import java.util.HashMap;

@NoArgsConstructor
@Getter
@Setter
public abstract class CommonAuthenticator implements IAuthenticator {
    private static Logger logger = LoggerFactory.getLogger(CommonAuthenticator.class);

    @Override
    public String[] signon(String remoteAddr, String user, String userPassword) throws Exception {
        return buildDefaults();
    }

    @Override
    public String[] generateToken(String remoteAddr, String refreshToken) throws Exception {
        return buildDefaults();
    }

    @Override
    public String getRoles(String remoteAddr, String currentToken) throws Exception {
        return null;
    }

    private String[] buildDefaults() {
        String[] returnValues = new String[2];
        returnValues[0] = "auth_factory_not_specified_thus_returning_default_value";
        returnValues[1] = "auth_factory_not_specified_thus_returning_default_value";

        return returnValues;
    }
}
