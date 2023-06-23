package gov.cdc.dataingestion.util;

import org.apache.http.HttpEntity;
import org.apache.http.auth.UsernamePasswordCredentials;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.auth.BasicScheme;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.util.EntityUtils;

public class AuthUtil {
    private static String result = "";

    public static String getString(String adminUser, char[] adminPassword, String serviceEndpoint) {
        try {
            UsernamePasswordCredentials credentials = new UsernamePasswordCredentials(adminUser, new String(adminPassword));

            CloseableHttpClient httpsClient = HttpClients.createDefault();
            HttpPost postRequest = new HttpPost(serviceEndpoint);
            postRequest.addHeader("accept", "*/*");
            postRequest.addHeader(BasicScheme.authenticate(credentials, "US-ASCII", false));

            CloseableHttpResponse response = httpsClient.execute(postRequest);

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
            httpsClient.close();
        } catch (Exception e) {
            result = "Exception occurred: " + e.getMessage();
        }
        return result;
    }
}
