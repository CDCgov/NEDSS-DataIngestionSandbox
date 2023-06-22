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

@CommandLine.Command(name = "token", mixinStandardHelpOptions = true, description = "Generates a JWT token.")
public class TokenGenerator implements Runnable {

    @Override
    public void run() {
        Console console = System.console();
        String result = "";
        String serviceEndpoint = "https://dataingestion.datateam-cdc-nbs.eqsandbox.com/token";
        System.out.println("Connecting to NBS Data Ingestion Service...");
        result = AuthUtil.getString(console, result, serviceEndpoint);
        System.out.println(result);
    }
}
