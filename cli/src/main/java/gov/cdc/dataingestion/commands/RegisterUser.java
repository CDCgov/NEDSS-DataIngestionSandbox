package gov.cdc.dataingestion.commands;

import gov.cdc.dataingestion.model.AuthModel;
import gov.cdc.dataingestion.util.AuthUtil;
import picocli.CommandLine;

import java.io.Console;

@CommandLine.Command(name = "register", mixinStandardHelpOptions = true, description = "Client will be onboarded providing username and secret.")
public class RegisterUser implements Runnable {

    @CommandLine.Option(names = {"--client-username"}, description = "Username provided by the client", interactive = true, echo = true, required = true)
    String username;

    @CommandLine.Option(names = {"--client-secret"}, description = "Secret provided by the client", interactive = true, required = true)
    char[] password;

    @CommandLine.Option(names = {"--admin-user"}, description = "Admin Username to connect to DI service", interactive = true, echo = true, required = true)
    String adminUser;

    @CommandLine.Option(names = {"--admin-password"}, description = "Admin Password to connect to DI service", interactive = true, required = true)
    char[] adminPassword;

    AuthModel authModel = new AuthModel();
    AuthUtil authUtil = new AuthUtil();


    @Override
    public void run() {
        if(username != null && password != null && adminUser != null && adminPassword != null) {
            if(!username.isEmpty() && password.length > 0 && !adminUser.isEmpty() && adminPassword.length > 0) {
                String serviceEndpoint = "https://dataingestion.datateam-cdc-nbs.eqsandbox.com/registration?username="
                        + username + "&password=" + new String(password);

                authModel.setAdminUser(adminUser);
                authModel.setAdminPassword(adminPassword);
                authModel.setServiceEndpoint(serviceEndpoint);

                String apiResponse = authUtil.getResponseFromDIService(authModel);
                if(apiResponse != null) {
                    if(apiResponse.contains("CREATED")) {
                        System.out.println("User onboarded successfully.");
                    }
                    else if(apiResponse.contains("NOT_ACCEPTABLE")) {
                        System.out.println("Username already exists. Please choose a unique client username.");
                    }
                    else {
                        System.out.println(apiResponse);
                    }
                }
                else {
                    System.err.println("Something went wrong with API. Response came back as null.");
                }

            }
            else {
                System.err.println("One or more inputs are empty.");
            }
        }
        else {
            System.err.println("One or more inputs are null.");
        }

    }
}
