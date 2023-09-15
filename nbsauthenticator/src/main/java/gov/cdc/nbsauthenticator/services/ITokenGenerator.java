package gov.cdc.nbsauthenticator.services;

import  java.util.HashMap;

public interface ITokenGenerator {
    String createToken(String remoteAddr, HashMap<String, Object> authClaims) throws Exception;
    String generateToken(String remoteAddr, String currentToken) throws Exception;
    boolean verifyToken(String remoteAddr, String currentToken) throws Exception;
    HashMap<String, String> getRoles(String remoteAddr, String currentToken);
}
