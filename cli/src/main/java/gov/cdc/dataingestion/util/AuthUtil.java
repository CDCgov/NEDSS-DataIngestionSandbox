package gov.cdc.dataingestion.util;

import org.apache.http.HttpEntity;
import org.apache.http.auth.UsernamePasswordCredentials;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.auth.BasicScheme;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.util.EntityUtils;

import java.io.Console;

public class AuthUtil {

    public static String getString(Console console, String result, String serviceEndpoint) {
        try {
            String adminUser = console.readLine("Enter admin username: ");
            char[] adminPassword = console.readPassword("Enter admin password: ");

//            final String auth = adminUser + ":" + new String(adminPassword);
//            final byte[] encodedAuth = Base64.encodeBase64(auth.getBytes(StandardCharsets.ISO_8859_1));
//            final String authHeader = "Basic " + new String(encodedAuth);

            UsernamePasswordCredentials creds = new UsernamePasswordCredentials(adminUser, new String(adminPassword));

//            CloseableHttpClient httpsClient = HttpClientBuilder.create()
//                    .setDefaultCredentialsProvider(provider)
//                    .build();
            CloseableHttpClient httpsClient = HttpClients.createDefault();

//            System.out.println("Password is printing..." + new String(adminPassword));

            HttpPost postRequest = new HttpPost(serviceEndpoint);
            postRequest.addHeader("accept", "*/*");
            postRequest.addHeader(BasicScheme.authenticate(creds, "US-ASCII", false));
//            postRequest.setHeader(HttpHeaders.AUTHORIZATION, authHeader);

            CloseableHttpResponse response = httpsClient.execute(postRequest);

//            System.out.println("Response status codeeee..." + response.getStatusLine().getStatusCode());

            if (response.getStatusLine().getStatusCode() == 200) {
                HttpEntity entity = response.getEntity();
                if (entity != null) {
                    result = EntityUtils.toString(entity);
                }
            } else if (response.getStatusLine().getStatusCode() == 401) {
                result = "Unauthorized. Admin username/password is incorrect.";
            } else {
                result = "Something went wrong on the server side. Please check the logs.";
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
        return result;
    }
}
