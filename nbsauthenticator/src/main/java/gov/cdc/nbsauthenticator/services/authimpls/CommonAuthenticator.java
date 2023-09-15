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
public class CommonAuthenticator implements IAuthenticator {
    private static Logger logger = LoggerFactory.getLogger(CommonAuthenticator.class);

    public String signon(String remoteAddr, String user, String userPassword) throws Exception {
        return null;
    }

    public String generateToken(String remoteAddr, String currentToken) throws Exception {
        return "to_be_implemented";
    }

    public HashMap<String, String> getRoles(String remoteAddr, String currentToken) throws Exception {
        return new HashMap<>();
    }
}
