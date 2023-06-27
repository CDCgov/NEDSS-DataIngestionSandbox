package gov.cdc.dataingestion.commands;

import gov.cdc.dataingestion.util.AuthUtil;
import picocli.CommandLine;

import java.io.Console;

@CommandLine.Command(name = "token", mixinStandardHelpOptions = true, description = "Generates a JWT token.")
public class TokenGenerator implements Runnable {

    @CommandLine.Option(names = {"--adminUser"}, description = "Admin Username to connect to DI service", interactive = true, echo = true, required = true)
    String adminUser;

    @CommandLine.Option(names = {"--adminPassword"}, description = "Admin Password to connect to DI service", interactive = true, required = true)
    char[] adminPassword;

    @Override
    public void run() {
//        Console console = System.console();
        if(adminUser != null && adminPassword != null) {
            if(!adminUser.isEmpty() && adminPassword.length > 0) {
                String serviceEndpoint = "https://dataingestion.datateam-cdc-nbs.eqsandbox.com/token";
                System.out.println("Connecting to NBS Data Ingestion Service...");
//        String adminUser = console.readLine("Enter admin username: ");
//        char[] adminPassword = console.readPassword("Enter admin password: ");
                String apiResponse = AuthUtil.getString(adminUser, adminPassword, serviceEndpoint);
                System.out.println(apiResponse);
            }
            else {
                System.err.println("Admin username or password is empty.");
            }
        }
        else {
            System.err.println("Admin username or password is null.");
        }

    }
}
