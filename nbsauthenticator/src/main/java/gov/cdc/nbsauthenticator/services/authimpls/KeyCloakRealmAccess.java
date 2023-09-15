package gov.cdc.nbsauthenticator.services.authimpls;

import  lombok.Getter;
import 	lombok.NoArgsConstructor;
import  lombok.Setter;

import  java.util.Date;

@NoArgsConstructor
@Setter
@Getter
public class KeyCloakRealmAccess {
    private String[] roles;
}