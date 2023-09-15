package gov.cdc.nbsauthenticator.services.authimpls;

import  lombok.Getter;
import 	lombok.NoArgsConstructor;
import  lombok.Setter;

import  java.util.Date;

@NoArgsConstructor
@Setter
@Getter
public class KeyCloakTokenDataHolder {
    private String access_token;
    private int expires_in;
    private int refresh_expires_in;
    private String refresh_token;
    private String token_type;
    private int policy;
    private String session_state;
    private String scope;
}