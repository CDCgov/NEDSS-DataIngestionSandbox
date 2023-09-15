package gov.cdc.nbsauthenticator.services.authimpls;

import gov.cdc.nbsauthenticator.repositories.NbsAuthUserRolesRepository;
import gov.cdc.nbsauthenticator.repositories.NbsAuthUsersRepository;
import  gov.cdc.nbsauthenticator.repositories.models.NbsAuthUserRoleModel;

import gov.cdc.nbsauthenticator.services.IAuthenticator;
import gov.cdc.nbsauthenticator.services.ITokenGenerator;
import gov.cdc.nbsauthenticator.services.TokenGenerator;
import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;
import	lombok.NoArgsConstructor;
import	lombok.Getter;
import	lombok.Setter;

import  org.slf4j.Logger;
import  org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import  org.springframework.stereotype.Component;

import javax.crypto.spec.SecretKeySpec;
import  java.math.BigInteger;
import java.security.Key;
import  java.util.Base64;
import  java.util.List;
import  java.util.HashMap;

@NoArgsConstructor
@Getter
@Setter
@Component
public class NbsClassicAuthAuthenticator extends CommonAuthenticator {
    private static Logger logger = LoggerFactory.getLogger(NbsClassicAuthAuthenticator.class);

    @Autowired
    private NbsAuthUsersRepository authUsersRepository;

    @Autowired
    private NbsAuthUserRolesRepository authRolesRepository;

    @Autowired
    private TokenGenerator tokenGenerator;


    @Override
    public String signon(String remoteAddr, String user, String userPassword) throws Exception {
        // Good: http://localhost:8090/nbsauth/signon?user=bmVkc3NfZWxyX2xvYWQ=&password=bmJzMjAyMw==
        // Bad : http://localhost:8090/nbsauth/signon?user=cmFtZXNo&password=bmJzMjAyMw==

        String clearUser = new String(Base64.getDecoder().decode(user));
        String clearPassword = new String(Base64.getDecoder().decode(userPassword));

        BigInteger authUserId = authUsersRepository.getAuthUserIdUsingUserIdAndPassword(clearUser, clearPassword);
        if(null == authUserId) return null;

        return createToken(remoteAddr, authUserId.intValue(), user);
    }

    @Override
    public HashMap<String, String> getRoles(String remoteAddr, String currentToken) throws Exception {
        return tokenGenerator.getRoles(remoteAddr, currentToken);
    }

    private String createToken(String remoteAddr, int authUserId, String user) throws Exception {
        List<NbsAuthUserRoleModel>  roles = authRolesRepository.getAuthRolesForAuthUserId(authUserId);

        StringBuffer programAreaCodes = new StringBuffer();
        StringBuffer authRoleNames = new StringBuffer();
        StringBuffer jurisdictionCodes = new StringBuffer();

        for(NbsAuthUserRoleModel roleModel : roles) {
            programAreaCodes.append(roleModel.getProgAreaCd());
            programAreaCodes.append(",");

            authRoleNames.append(roleModel.getAuthRoleNm());
            authRoleNames.append(",");

            jurisdictionCodes.append(roleModel.getJurisdictionCd());
            jurisdictionCodes.append(",");
        }

        HashMap<String, Object> authClaims = new HashMap<>();

        if(programAreaCodes.length() > 0) {
            authClaims.put("prog_area_cd", programAreaCodes.toString());
        }

        if( authRoleNames.length() > 0) {
            authClaims.put("auth_role_nm", authRoleNames.toString());
        }

        if(jurisdictionCodes.length() > 0) {
            authClaims.put("jurisdiction_cd", jurisdictionCodes.toString());
        }

        authClaims.put("auth_user", user);
        authClaims.put("auth_user_id", String.valueOf(authUserId));

        String token = tokenGenerator.createToken(remoteAddr, authClaims);

        return token;
    }

    @Override
    public String generateToken(String remoteAddr, String currentToken) throws Exception {
        boolean isCurrentTokenValid = getTokenGenerator().verifyToken(remoteAddr, currentToken);
        if(!isCurrentTokenValid) {
            throw new Exception("Invalid token, please signon again");
        }

        String newToken = tokenGenerator.generateToken(remoteAddr, currentToken);

        return newToken;
    }
}
