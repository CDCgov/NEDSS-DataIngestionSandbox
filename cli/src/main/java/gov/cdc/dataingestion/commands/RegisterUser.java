package gov.cdc.dataingestion.commands;

import gov.cdc.dataingestion.util.AuthUtil;
import picocli.CommandLine;

import java.io.Console;

@CommandLine.Command(name = "register", mixinStandardHelpOptions = true, description = "Client will be onboarded providing username and secret.")
public class RegisterUser implements Runnable {

    @CommandLine.Option(names = {"--username"}, required = true, description = "Username provided by the client.")
    String username;

    @CommandLine.Option(names = {"--secret"}, description = "Secret provided by the client", interactive = true)
    char[] password;


    @Override
    public void run() {
        Console console = System.console();
        if (password == null && console != null) {
            password = console.readPassword("Enter the secret provided by the client (CASE-SENSITIVE):");
        }
        String serviceEndpoint = "https://dataingestion.datateam-cdc-nbs.eqsandbox.com/registration?username="
                + username + "&password=" + new String(password);
        System.out.println("Connecting to NBS Data Ingestion Service...");
        String adminUser = console.readLine("Enter admin username: ");
        char[] adminPassword = console.readPassword("Enter admin password: ");
        String apiResponse = AuthUtil.getString(adminUser, adminPassword, serviceEndpoint);
        if(apiResponse.contains("CREATED")) {
            System.out.println("User onboarded successfully.");
        }
        else if(apiResponse.contains("NOT_ACCEPTABLE")) {
            System.out.println("Username already exists. Please choose a unique client username.");
        }
    }
}
