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

import  org.json.JSONObject;

import  java.util.Base64;

@Component
public class AuthIntegrator implements ApplicationListener<ApplicationReadyEvent> {
    private static Logger logger = LoggerFactory.getLogger(AuthIntegrator.class);
    private static String AUTH_ROLE_CLAIM = "auth_role_nm";
    private static String AUTH_ELR_CLAIM = "ELR Importer";
    private static String AUTH_ECR_CLAIM = "ECR Importer";

    @Value("${auth.url}")
    private String url;

    @Value("${auth.user}")
    private String nbsUser;

    @Value("${auth.password}")
    private String nbsUserPassword;

    @Override
    public void onApplicationEvent(final ApplicationReadyEvent event) {
        try {
            String signonUrl = getSignonUrl();
            logger.info("Signon url = {}", signonUrl);

            String token = getToken(signonUrl);
            if (null == token) {
                logger.error("Authentication failed, token is null, thus returning");
                return;
            }

            logger.info("Token = {}", token);

            String rolesUrl = String.format("%s/nbsauth/roles", url);
            logger.info("Roles url = {}", rolesUrl);

            String authRoleName = getRoles(rolesUrl, token);
            if (null == authRoleName) {
                logger.error("Auth roles not defined, nothing to authorize, thus returning");
                return;
            }

            logger.info("Auth role claim = {}", authRoleName);

            boolean isAllowedToLoadElrData = authRoleName.contains(AUTH_ELR_CLAIM) || authRoleName.contains("allow_elr_data_loading");
            boolean isAllowedToLoadEcrData = authRoleName.contains(AUTH_ECR_CLAIM) || authRoleName.contains("allow_ecr_data_loading");

            logger.info("Is allowed to load ELR data = {}", isAllowedToLoadElrData);
            logger.info("Is allowed to load ECR data = {}", isAllowedToLoadEcrData);
        }
        catch(Exception e) {
            logger.error("Error observed!", e);
        }

    }

    private String getRoles(String rolesUrl, String token) throws Exception {
        String rolesString = getResponse(rolesUrl, token);
        JSONObject jsonObj = new JSONObject(rolesString);
        return (String) jsonObj.get("roles");
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

    private String getToken(String signonUrl) throws Exception {
        String tokenString = getResponse(signonUrl, "");
        JSONObject jsonObj = new JSONObject(tokenString);
        return (String) jsonObj.get("token");
    }

    private String getResponse(String requestUrl, String token) throws Exception {
        if( requestUrl.startsWith("https") ) {
            disableTrustStore();
        }

        URL url = new URL(requestUrl);
        URLConnection con = url.openConnection();

        if( requestUrl.startsWith("https") ) {
            HttpsURLConnection https = (HttpsURLConnection) con;
            https.setRequestMethod("POST");

            if(token.length() > 0) {
                https.setRequestProperty("Auth-Token", token);
            }
        }
        else {
            HttpURLConnection http = (HttpURLConnection) con;
            http.setRequestMethod("POST");

            if(token.length() > 0) {
                http.setRequestProperty("Auth-Token", token);
            }
        }



        final Reader reader = new InputStreamReader(con.getInputStream());
        final BufferedReader br = new BufferedReader(reader);

        String line = "";
        String responseString = "";
        while ((line = br.readLine()) != null) {
            responseString += line;
        }

        br.close();
        return responseString;
    }

    private void disableTrustStore() throws Exception {
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

        final SSLContext sc = SSLContext.getInstance("SSL");
        sc.init(null, trustAllCerts, new java.security.SecureRandom());
        HttpsURLConnection.setDefaultSSLSocketFactory(sc.getSocketFactory());

        HostnameVerifier allHostsValid = new HostnameVerifier() {
            public boolean verify(String hostname, SSLSession session) {
                return true;
            }
        };

        HttpsURLConnection.setDefaultHostnameVerifier(allHostsValid);
    }
}
