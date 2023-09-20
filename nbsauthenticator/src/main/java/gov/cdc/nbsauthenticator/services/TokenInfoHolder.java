package gov.cdc.nbsauthenticator.services;

import  lombok.Getter;
import 	lombok.NoArgsConstructor;
import  lombok.Setter;

import  java.util.Date;

@NoArgsConstructor
@Setter
@Getter
public class TokenInfoHolder {
    private String remoteAddress;
    private String token;
    private Date expiration;
    private String refreshToken;
}