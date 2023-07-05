package gov.cdc.dataingestion.util;

import org.apache.http.Header;
import org.apache.http.HttpEntity;
import org.apache.http.auth.UsernamePasswordCredentials;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.auth.BasicScheme;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.util.EntityUtils;

import java.io.*;
import java.nio.charset.StandardCharsets;

public class AuthUtil {

    public String getResponseFromApi(String adminUser, char[] adminPassword, String serviceEndpoint) {
        try {
            UsernamePasswordCredentials credentials = new UsernamePasswordCredentials(adminUser, new String(adminPassword));

            CloseableHttpClient httpsClient = HttpClients.createDefault();
            HttpPost postRequest = new HttpPost(serviceEndpoint);
            Header authHeader = new BasicScheme(StandardCharsets.UTF_8).authenticate(credentials, postRequest, null);
            postRequest.addHeader("accept", "*/*");
            postRequest.addHeader(authHeader);

            CloseableHttpResponse response = httpsClient.execute(postRequest);
            int statusCode = response.getStatusLine().getStatusCode();

            if (statusCode == 200) {
                InputStream content = response.getEntity().getContent();
                String result = convertInputStreamToString(content);
                httpsClient.close();
                return result;
            } else if (response.getStatusLine().getStatusCode() == 401) {
                httpsClient.close();
                return "Unauthorized. Admin username/password is incorrect.";
            } else {
                httpsClient.close();
                return "Something went wrong on the server side. Please check the logs.";
            }
        } catch (Exception e) {
                return "Exception occurred: " + e.getMessage();
        }
    }

    private String convertInputStreamToString(InputStream content) throws IOException {
        BufferedReader reader = new BufferedReader(new InputStreamReader(content));
        StringBuilder stringBuilder = new StringBuilder();
        String line;
        while ((line = reader.readLine()) != null) {
            stringBuilder.append(line);
        }
        return stringBuilder.toString();
    }
}
