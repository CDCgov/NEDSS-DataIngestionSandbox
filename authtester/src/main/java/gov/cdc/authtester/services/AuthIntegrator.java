package gov.cdc.authtester.services;

import  org.springframework.beans.factory.annotation.Value;
import  org.springframework.stereotype.Component;
import  org.springframework.context.ApplicationListener;
import  org.springframework.boot.context.event.ApplicationReadyEvent;

import  org.slf4j.Logger;
import  org.slf4j.LoggerFactory;

import  java.net.URL;
import  java.net.URLConnection;
import  java.io.Reader;
import  java.io.InputStreamReader;
import  java.io.BufferedReader;
import  java.net.HttpURLConnection;
import  javax.net.ssl.TrustManager;
import  javax.net.ssl.X509TrustManager;
import  javax.net.ssl.SSLContext;
import  javax.net.ssl.HttpsURLConnection;
import  javax.net.ssl.HostnameVerifier;
import  javax.net.ssl.SSLSession;
import  java.security.cert.X509Certificate;

import  io.jsonwebtoken.Claims;
import  io.jsonwebtoken.Jwts;
import  io.jsonwebtoken.SignatureAlgorithm;
import  javax.crypto.spec.SecretKeySpec;
import  java.security.Key;

import  java.util.Base64;

import  com.google.gson.Gson;

@Component
public class AuthIntegrator implements ApplicationListener<ApplicationReadyEvent> {
    private static Logger logger = LoggerFactory.getLogger(AuthIntegrator.class);
    private static String AUTH_ROLE_CLAIM = "auth_role_nm";
    private static String AUTH_ELR_CLAIM = "ELR Importer";
    private static String AUTH_ECR_CLAIM = "ECR Importer";

    @Value("${auth.url}")
    private String url;

    @Value("${auth.secretforalgorithm}")
    private String secretForAlgorithm;

    @Value("${auth.user}")
    private String nbsUser;

    @Value("${auth.password}")
    private String nbsUserPassword;

    @Override
    public void onApplicationEvent(final ApplicationReadyEvent event) {
        String signonUrl = getSignonUrl();
        logger.info("Signon url = {}", signonUrl);

        String token = getToken(signonUrl);
        if(null == token) {
            logger.error("Authentication failed, token is null, thus returning");
            return;
        }

        logger.info("Token = {}", token);

        String authRoleName = getAuthRoleClaim(token);
        if(null == authRoleName) {
            logger.error("Auth roles not defined, nothing to authorize, thus returning");
            return;
        }

        logger.info("Auth role claim = {}", authRoleName);

        boolean isAllowedToLoadElrData = authRoleName.contains(AUTH_ELR_CLAIM);
        boolean isAllowedToLoadEcrData = authRoleName.contains(AUTH_ECR_CLAIM);

        logger.info("Is allowed to load ELR data = {}", isAllowedToLoadElrData);
        logger.info("Is allowed to load ECR data = {}", isAllowedToLoadEcrData);

    }

    private String getAuthRoleClaim(String token) {
        Key hmacKey = new SecretKeySpec(secretForAlgorithm.getBytes(), SignatureAlgorithm.HS256.getJcaName());
        Claims jwtClaims = Jwts.parserBuilder()
                .setSigningKey(hmacKey)
                .build()
                .parseClaimsJws(token)
                .getBody();

        //displayClaims(jwtClaims);

        return (String) jwtClaims.get(AUTH_ROLE_CLAIM);
    }

    private void displayClaims(Claims jwtClaims) {
        for(String claimKey : jwtClaims.keySet()) {
            logger.info("Claim key = {}, Claim = {}", claimKey, jwtClaims.get(claimKey));
        }
    }

    private String getSignonUrl() {
        String encryptedUser = new String(Base64.getEncoder().encode(nbsUser.getBytes()));
        String encryptedPassword = new String(Base64.getEncoder().encode(nbsUserPassword.getBytes()));

        String strUrl = String.format("%s/nbsauth/signon?user=%s&password=%s",
                            url,
                            encryptedUser,
                            encryptedPassword);

        return strUrl;
    }

    private String getToken(String signonUrl) {
        try {
            if( signonUrl.startsWith("https") ) {
                // Create a trust manager that does not validate certificate chains
                TrustManager[] trustAllCerts = new TrustManager[]{
                        new X509TrustManager() {
                            public java.security.cert.X509Certificate[] getAcceptedIssuers() {
                                return null;
                            }

                            public void checkClientTrusted(X509Certificate[] certs, String authType) {
                            }

                            public void checkServerTrusted(X509Certificate[] certs, String authType) {
                            }
                        }
                };

                // Install the all-trusting trust manager
                final SSLContext sc = SSLContext.getInstance("SSL");
                sc.init(null, trustAllCerts, new java.security.SecureRandom());
                HttpsURLConnection.setDefaultSSLSocketFactory(sc.getSocketFactory());

                // Create all-trusting host name verifier
                HostnameVerifier allHostsValid = new HostnameVerifier() {
                    public boolean verify(String hostname, SSLSession session) {
                        return true;
                    }
                };

                // Install the all-trusting host verifier
                HttpsURLConnection.setDefaultHostnameVerifier(allHostsValid);
            }

            URL url = new URL(signonUrl);
            URLConnection con = url.openConnection();

            if( signonUrl.startsWith("https") ) {
                HttpsURLConnection https = (HttpsURLConnection) con;
                https.setRequestMethod("POST");
            }
            else {
                HttpURLConnection http = (HttpURLConnection) con;
                http.setRequestMethod("POST");
            }

            final Reader reader = new InputStreamReader(con.getInputStream());
            final BufferedReader br = new BufferedReader(reader);

            String line = "";
            String tokenString = null;
            while ((line = br.readLine()) != null) {
                //logger.info("Received data from server = {}", line);
                if(line.indexOf("token") > 0) {
                    tokenString = line;
                }
            }

            br.close();

            Gson g = new Gson();
            TokenInfoHolder tokenInfo = g.fromJson(tokenString, TokenInfoHolder.class);
            //logger.info("Token = {}", tokenInfo.getToken()); //John

            return tokenInfo.getToken();
        }
        catch(Exception e) {
            logger.error("Exception observed, {}", e.toString());
        }

        return null;
    }
}
