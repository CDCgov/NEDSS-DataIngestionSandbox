package gov.cdc.dataingestion.commands;

import org.apache.http.HttpEntity;
import org.apache.http.auth.UsernamePasswordCredentials;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.auth.BasicScheme;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.util.EntityUtils;
import picocli.CommandLine;

import java.io.Console;
import java.util.concurrent.Callable;

@CommandLine.Command(name = "register", mixinStandardHelpOptions = true, description = "Client will be onboarded providing username and secret.")
public class RegisterUser implements Callable<String> {

    @CommandLine.Option(names = {"--username"}, required = true, description = "Username provided by the client.")
    String username;

    @CommandLine.Option(names = {"--secret"}, description = "Secret provided by the client", interactive = true)
    char[] password;


    @Override
    public String call() {
        Console console = System.console();
        String result = "Created?";
        if (password == null && console != null) {
            password = console.readPassword("Enter the secret provided by the client (CASE-SENSITIVE):");
        }
        System.out.println("Connecting to NBS Data Ingestion Service...");
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

            System.out.println("Password is printing..." + new String(password));

            HttpPost postRequest = new HttpPost("https://dataingestion.datateam-cdc-nbs.eqsandbox.com/registration?username="+ username +"&password="+new String(password));
            postRequest.addHeader("accept", "*/*");
            postRequest.addHeader(BasicScheme.authenticate(creds, "US-ASCII", false));
//            postRequest.setHeader(HttpHeaders.AUTHORIZATION, authHeader);

            CloseableHttpResponse response = httpsClient.execute(postRequest);

            System.out.println("Response status code..." + response.getStatusLine());

            HttpEntity entity = response.getEntity();
            if (entity != null) {
                // return it as a String
                result = EntityUtils.toString(entity);
                System.out.println(result);
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
        return result;
    }
}
