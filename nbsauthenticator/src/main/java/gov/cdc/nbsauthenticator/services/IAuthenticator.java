package gov.cdc.nbsauthenticator.services;

import  java.util.HashMap;

public interface IAuthenticator {
    String signon(String remoteAddr, String user, String userPassword) throws Exception;
    String generateToken(String remoteAddr, String currentToken) throws Exception;
    HashMap<String, String> getRoles(String remoteAddr, String currentToken) throws Exception;
}
