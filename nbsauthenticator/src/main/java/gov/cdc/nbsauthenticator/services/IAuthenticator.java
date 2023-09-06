package gov.cdc.nbsauthenticator.services;

import  gov.cdc.nbsauthenticator.repositories.NbsAuthUsersRepository;
import  gov.cdc.nbsauthenticator.repositories.NbsAuthUserRolesRepository;
import org.aspectj.weaver.patterns.IToken;

import  java.util.List;

public interface IAuthenticator {
    int signon(String user, String userPassword);
    String createToken(String remoteAddr, int authUserId, String user) throws Exception;
    String generateToken(String remoteAddr, String currentToken) throws Exception;

    void setAuthUserRepository(NbsAuthUsersRepository authUserRepository);
    void setAuthRolesRepository(NbsAuthUserRolesRepository authRolesRepository);
    void setTokenGenerator(ITokenGenerator tokenGenerator);
}
