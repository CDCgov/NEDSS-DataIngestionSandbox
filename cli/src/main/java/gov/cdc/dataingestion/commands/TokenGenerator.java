package gov.cdc.dataingestion.commands;

import gov.cdc.dataingestion.model.AuthModel;
import gov.cdc.dataingestion.util.AuthUtil;
import picocli.CommandLine;

@CommandLine.Command(name = "token", mixinStandardHelpOptions = true, description = "Generates a JWT token.")
public class TokenGenerator implements Runnable {

    @CommandLine.Option(names = {"--admin-user"}, description = "Admin Username to connect to DI service", interactive = true, echo = true, required = true)
    String adminUser;

    @CommandLine.Option(names = {"--admin-password"}, description = "Admin Password to connect to DI service", interactive = true, required = true)
    char[] adminPassword;

    AuthModel authModel = new AuthModel();
    AuthUtil authUtil = new AuthUtil();

    @Override
    public void run() {
        if(adminUser != null && adminPassword != null) {
            if(!adminUser.isEmpty() && adminPassword.length > 0) {
                String serviceEndpoint = "https://dataingestion.datateam-cdc-nbs.eqsandbox.com/token";

                authModel.setAdminUser(adminUser);
                authModel.setAdminPassword(adminPassword);
                authModel.setServiceEndpoint(serviceEndpoint);

                String apiResponse = authUtil.getResponseFromDIService(authModel);
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
