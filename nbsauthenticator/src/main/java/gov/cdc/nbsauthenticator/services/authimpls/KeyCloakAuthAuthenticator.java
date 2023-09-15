package gov.cdc.nbsauthenticator.services.authimpls;

import com.google.gson.Gson;
import	lombok.NoArgsConstructor;
import	lombok.Getter;
import	lombok.Setter;

import  org.apache.http.impl.client.CloseableHttpClient;
import  org.slf4j.Logger;
import  org.slf4j.LoggerFactory;
import  org.springframework.beans.factory.annotation.Value;
import  org.springframework.stereotype.Component;

import javax.net.ssl.*;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.Reader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLConnection;
import java.security.cert.X509Certificate;

import java.nio.charset.StandardCharsets;
import java.io.DataOutputStream;
import java.util.Base64;
import java.util.HashMap;

@NoArgsConstructor
@Getter
@Setter
@Component
public class KeyCloakAuthAuthenticator extends CommonAuthenticator {
    private static Logger logger = LoggerFactory.getLogger(KeyCloakAuthAuthenticator.class);
    private static Gson gson = new Gson();

    @Value("${auth.keycloak.url}")
    private String url;

    @Value("${auth.keycloak.infourl}")
    private String infourl;

    @Value("${auth.keycloak.clientid}")
    private String clientId;

    @Value("${auth.keycloak.clientsecret}")
    private String clientSecret;

    private CloseableHttpClient httpClient = null;

    @Override
    public String signon(String remoteAddr, String user, String userPassword) throws Exception {
        String clearUser = new String(Base64.getDecoder().decode(user));
        String clearPassword = new String(Base64.getDecoder().decode(userPassword));

        String urlParameters  = String.format("username=%s&password=%s&client_id=%s&client_secret=%s&grant_type=password",
                clearUser,
                clearPassword,
                clientId,
                clientSecret);

        String response = getResponse(url, urlParameters);
        if(response.indexOf("access_token") > -1) {
            KeyCloakTokenDataHolder data = gson.fromJson(response, KeyCloakTokenDataHolder.class);
            return data.getAccess_token();
        }

        logger.info("signonResponseString = " + response);
        return null;
    }

    @Override
    public HashMap<String, String> getRoles(String remoteAddr, String currentToken) throws Exception {
        String urlParameters  = String.format("client_id=%s&client_secret=%s&token=%s",
                clientId,
                clientSecret,
                currentToken);

        String response = getResponse(infourl, urlParameters);
        if(response.indexOf("realm_access") > -1) {
            KeyCloakTokenInfoHolder info = gson.fromJson(response, KeyCloakTokenInfoHolder.class);
            String[] roles = info.getRealm_access().getRoles();
            HashMap<String, String> mapOfRoles = new HashMap<>();
            for(String s : roles) {
                mapOfRoles.put(s, s);
            }

            return mapOfRoles;
        }

        return null;
    }

    private HttpsURLConnection initializeHttpsConnection(URLConnection con, int postDataLength) throws Exception {
        HttpsURLConnection https = (HttpsURLConnection) con;

        https.setDoOutput(true);
        https.setInstanceFollowRedirects(false);
        https.setRequestMethod("POST");
        https.setRequestProperty("Content-Type", "application/x-www-form-urlencoded");
        https.setRequestProperty("charset", "utf-8");
        https.setRequestProperty("Content-Length", Integer.toString(postDataLength));
        https.setUseCaches(false);

        return https;
    }

    private HttpURLConnection initializeHttpConnection(URLConnection con, int postDataLength) throws Exception {
        HttpURLConnection http = (HttpURLConnection) con;

        http.setDoOutput(true);
        http.setInstanceFollowRedirects(false);
        http.setRequestMethod("POST");
        http.setRequestProperty("Content-Type", "application/x-www-form-urlencoded");
        http.setRequestProperty("charset", "utf-8");
        http.setRequestProperty("Content-Length", Integer.toString(postDataLength));
        http.setUseCaches(false);

        return http;
    }

    private String getResponse(String urlToInvoke, String urlParameters)  throws Exception {
        if( urlToInvoke.startsWith("https")) {
            disableTrustStore();
        }

        URL connUrl = new URL(urlToInvoke);
        URLConnection con = connUrl.openConnection();

        byte[] postData = urlParameters.getBytes( StandardCharsets.UTF_8 );
        int postDataLength = postData.length;

        if (urlToInvoke.startsWith("https")) {
            HttpsURLConnection https = initializeHttpsConnection(con, postDataLength);
            try(DataOutputStream wr = new DataOutputStream(https.getOutputStream())) {
                wr.write( postData );
            }

        } else {
            HttpURLConnection http = initializeHttpConnection(con, postDataLength);
            try(DataOutputStream wr = new DataOutputStream(http.getOutputStream())) {
                wr.write(postData);
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
