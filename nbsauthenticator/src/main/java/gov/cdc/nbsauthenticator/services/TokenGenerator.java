package gov.cdc.nbsauthenticator.services;

import 	org.springframework.stereotype.Service;
import 	org.springframework.beans.factory.annotation.Value;

import 	lombok.NoArgsConstructor;

import  io.jsonwebtoken.Claims;
import  io.jsonwebtoken.Jwts;
import  io.jsonwebtoken.JwtBuilder;
import  io.jsonwebtoken.SignatureAlgorithm;
import  javax.crypto.spec.SecretKeySpec;
import  java.security.Key;

import  java.util.Map;
import  java.util.Set;
import	java.util.UUID;
import	java.util.Date;
import  java.util.HashMap;
import	java.time.Instant;
import	java.time.temporal.ChronoUnit;

import  org.slf4j.Logger;
import  org.slf4j.LoggerFactory;

@Service
@NoArgsConstructor
public class TokenGenerator implements ITokenGenerator {
    private static final int TOKEN_MAX_VALID_PERIOD = 1;
	private static Logger logger = LoggerFactory.getLogger(TokenGenerator.class);
    private static HashMap<String, TokenInfoHolder> tokensMap = new HashMap<>();

    @Value("${auth.nbsclassic.secretforalgorithm}")
    private String secretForAlgorithm = "A picture is worth a thousand words. Implies, artwork or images can convey meanings that go beyond verbal description.";

    @Value("${spring.application.name}")
    private String claimSubject;

    private long lAllowed = TOKEN_MAX_VALID_PERIOD * 3600 * 1000;

    @Override
    public boolean verifyToken(String remoteAddr,String currentToken) {
        boolean isValid = false;
        TokenInfoHolder tih = null;

        synchronized ( tokensMap ) {
            tih = (TokenInfoHolder) tokensMap.get(remoteAddr);
        }

        if(null == tih) {
            return isValid;
        }

        Date now = new Date();
        long lDuration = now.getTime() - tih.getExpiration().getTime();
        isValid = ((lAllowed - lDuration) > 0);

        return isValid;
    }

    public String getRoles(String remoteAddr, String currentToken) {
        Key hmacKey = new SecretKeySpec(secretForAlgorithm.getBytes(), SignatureAlgorithm.HS256.getJcaName());
        Claims jwtClaims = Jwts.parserBuilder()
                .setSigningKey(hmacKey)
                .build()
                .parseClaimsJws(currentToken)
                .getBody();

        return (String) jwtClaims.get("auth_role_nm");
    }

    @Override
    public String generateToken(String remoteAddr, String currentToken) throws Exception {
        Key hmacKey = new SecretKeySpec(secretForAlgorithm.getBytes(), SignatureAlgorithm.HS256.getJcaName());

        Claims jwtClaims = Jwts.parserBuilder()
                    .setSigningKey(hmacKey)
                    .build()
                    .parseClaimsJws(currentToken)
                    .getBody();

        HashMap<String, Object> mapOfClaims = new HashMap<>();
        for(String claimKey : jwtClaims.keySet()) {
            mapOfClaims.put(claimKey, jwtClaims.get(claimKey));
        }

        String newToken = createToken(remoteAddr, mapOfClaims);

        return newToken;
    }

    @Override
    public String createToken(String remoteAddr, HashMap<String, Object> authClaims) throws Exception {
        String jwtToken = null;

        try {
            Key hmacKey = new SecretKeySpec(secretForAlgorithm.getBytes(), SignatureAlgorithm.HS256.getJcaName());

            Instant now = Instant.now();
            Date expiration = Date.from(now.plus(TOKEN_MAX_VALID_PERIOD, ChronoUnit.HOURS));

            JwtBuilder jwtBuilder = Jwts.builder();

            for (Map.Entry<String, Object> claim : authClaims.entrySet()) {
                jwtBuilder.claim(claim.getKey(), claim.getValue());
            }

            jwtToken = jwtBuilder.setSubject(claimSubject)
                        .setId(UUID.randomUUID().toString())
                        .setIssuedAt(Date.from(now))
                        .setExpiration(expiration)
                        .signWith(hmacKey)
                        .compact();

            storeToken(remoteAddr, expiration, jwtToken);

            return jwtToken;
        }
        catch(Exception e) {
            logger.error(e.getMessage());
            throw e;
        }
    }

    private void storeToken(String remoteAddr, Date expiration, String jwtToken) {
        TokenInfoHolder tih = new TokenInfoHolder();
        tih.setRemoteAddress(remoteAddr);
        tih.setToken(jwtToken);
        tih.setExpiration(expiration);

        synchronized ( tokensMap ) {
            tokensMap.put(remoteAddr, tih);
        }
    }
}
