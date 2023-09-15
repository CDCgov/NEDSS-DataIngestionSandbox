package gov.cdc.nbsauthenticator.services.authimpls;

import  lombok.Getter;
import 	lombok.NoArgsConstructor;
import  lombok.Setter;

import  java.util.Date;

@NoArgsConstructor
@Setter
@Getter
public class KeyCloakTokenInfoHolder {
    private int exp;
    private int iat;
    private String jti;
    private String iss;
    private String aud;
    private String sub;
    private String type;
    private String azp;
    private String session_state;
    private String name;
    private String given_name;
    private String family_name;
    private String preferred_username;
    private boolean email_verified;
    private String acr;
    private KeyCloakRealmAccess realm_access;


    /*

        "realm_access": {
            "roles": [
                "default-roles-nbsauth",
                "offline_access",
                "allow_elr_data_loading",
                "uma_authorization"
            ]
        },
        "resource_access": {
            "account": {
                "roles": [
                    "manage-account",
                    "manage-account-links",
                    "view-profile"
                ]
            }
        },
        "scope": "email profile",
        "sid": "926beebe-486f-4cbb-997a-c11e1c680816",
        "client_id": "sysservices",
        "username": "elrloader",
        "active": true
    }
     */
}