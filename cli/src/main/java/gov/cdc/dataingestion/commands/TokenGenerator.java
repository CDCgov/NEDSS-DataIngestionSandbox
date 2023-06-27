package gov.cdc.dataingestion.commands;

import gov.cdc.dataingestion.util.AuthUtil;
import picocli.CommandLine;

@CommandLine.Command(name = "token", mixinStandardHelpOptions = true, description = "Generates a JWT token.")
public class TokenGenerator implements Runnable {

    @CommandLine.Option(names = {"--adminUser"}, description = "Admin Username to connect to DI service", interactive = true, echo = true, required = true)
    String adminUser;

    @CommandLine.Option(names = {"--adminPassword"}, description = "Admin Password to connect to DI service", interactive = true, required = true)
    char[] adminPassword;

    AuthUtil authUtil = new AuthUtil();

    @Override
    public void run() {
        if(adminUser != null && adminPassword != null) {
            if(!adminUser.isEmpty() && adminPassword.length > 0) {
                String serviceEndpoint = "https://dataingestion.datateam-cdc-nbs.eqsandbox.com/token";
                String apiResponse = authUtil.getResponseFromApi(adminUser, adminPassword, serviceEndpoint);
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
