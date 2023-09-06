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

@NoArgsConstructor
@Getter
@Setter
public class CommonAuthenticator implements IAuthenticator {
    private static Logger logger = LoggerFactory.getLogger(NbsClassicAuthAuthenticator.class);

    private NbsAuthUsersRepository authUsersRepo;
    private NbsAuthUserRolesRepository authRolesRepo;
    private ITokenGenerator tokenGenerator;

    public void setAuthUserRepository(NbsAuthUsersRepository authUsersRepo) {
        this.authUsersRepo = authUsersRepo;
    }
    public void setAuthRolesRepository(NbsAuthUserRolesRepository authRolesRepo) {
        this.authRolesRepo = authRolesRepo;
    }

    public int signon(String user, String userPassword) {
        return -1;
    }
    public String createToken(String remoteAddr, int authUserId, String user) throws Exception {
        return "to_be_implemented";
    }

    public String generateToken(String remoteAddr, String currentToken) throws Exception {
        return "to_be_implemented";
    }

    public void setTokenGenerator(ITokenGenerator tokenGenerator) {
        this.tokenGenerator = tokenGenerator;
    }
}
