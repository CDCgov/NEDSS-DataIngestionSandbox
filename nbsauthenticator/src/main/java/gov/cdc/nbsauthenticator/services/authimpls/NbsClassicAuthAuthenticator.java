package gov.cdc.nbsauthenticator.services.authimpls;

import  gov.cdc.nbsauthenticator.repositories.models.NbsAuthUserRoleModel;

import	lombok.NoArgsConstructor;
import	lombok.Getter;
import	lombok.Setter;

import  org.slf4j.Logger;
import  org.slf4j.LoggerFactory;

import  java.math.BigInteger;
import  java.util.Base64;
import  java.util.List;
import  java.util.HashMap;

@NoArgsConstructor
@Getter
@Setter
public class NbsClassicAuthAuthenticator extends CommonAuthenticator {
    private static Logger logger = LoggerFactory.getLogger(NbsClassicAuthAuthenticator.class);

    @Override
    public int signon(String user, String userPassword) {
        // Good: http://localhost:8090/nbsauth/signon?user=bmVkc3NfZWxyX2xvYWQ=&password=bmJzMjAyMw==
        // Bad : http://localhost:8090/nbsauth/signon?user=cmFtZXNo&password=bmJzMjAyMw==

        String clearUser = new String(Base64.getDecoder().decode(user));
        String clearPassword = new String(Base64.getDecoder().decode(userPassword));

        BigInteger authUserId = getAuthUsersRepo().getAuthUserIdUsingUserIdAndPassword(clearUser, clearPassword);
        if(null == authUserId) return -1;

        return authUserId.intValue();
    }

    @Override
    public String createToken(String remoteAddr, int authUserId, String user) throws Exception {
        List<NbsAuthUserRoleModel>  roles = getAuthRolesRepo().getAuthRolesForAuthUserId(authUserId);

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

        String token = getTokenGenerator().createToken(remoteAddr, authClaims);

        return token;
    }

    @Override
    public String generateToken(String remoteAddr, String currentToken) throws Exception {
        boolean isCurrentTokenValid = getTokenGenerator().verifyToken(remoteAddr, currentToken);
        if(!isCurrentTokenValid) {
            throw new Exception("Invalid token, please signon again");
        }

        String newToken = getTokenGenerator().generateToken(remoteAddr, currentToken);

        return newToken;
    }
}
