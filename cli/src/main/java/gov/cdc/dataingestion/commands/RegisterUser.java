package gov.cdc.dataingestion.commands;

import gov.cdc.dataingestion.util.AuthUtil;
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
public class RegisterUser implements Runnable {

    @CommandLine.Option(names = {"--username"}, required = true, description = "Username provided by the client.")
    String username;

    @CommandLine.Option(names = {"--secret"}, description = "Secret provided by the client", interactive = true)
    char[] password;


    @Override
    public void run() {
        Console console = System.console();
        String result = "";
        if (password == null && console != null) {
            password = console.readPassword("Enter the secret provided by the client (CASE-SENSITIVE):");
        }
        String serviceEndpoint = "https://dataingestion.datateam-cdc-nbs.eqsandbox.com/registration?username="
                + username + "&password=" + new String(password);
        System.out.println("Connecting to NBS Data Ingestion Service...");
        result = AuthUtil.getString(console, result, serviceEndpoint);
        if(result.contains("CREATED")) {
            System.out.println("User onboarded successfully.");
        }
        else if(result.contains("NOT_ACCEPTABLE")) {
            System.out.println("Username already exists. Please choose a unique client username.");
        }
    }
}
