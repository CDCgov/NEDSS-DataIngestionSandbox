package gov.cdc.dataingestion.commands;

import gov.cdc.dataingestion.util.AuthUtil;
import picocli.CommandLine;

import java.io.Console;

@CommandLine.Command(name = "token", mixinStandardHelpOptions = true, description = "Generates a JWT token.")
public class TokenGenerator implements Runnable {

    @Override
    public void run() {
        Console console = System.console();
        String serviceEndpoint = "https://dataingestion.datateam-cdc-nbs.eqsandbox.com/token";
        System.out.println("Connecting to NBS Data Ingestion Service...");
        String adminUser = console.readLine("Enter admin username: ");
        char[] adminPassword = console.readPassword("Enter admin password: ");
        String apiResponse = AuthUtil.getString(adminUser, adminPassword, serviceEndpoint);
        System.out.println(apiResponse);
    }
}
