package gov.cdc.dataingestion;

import gov.cdc.dataingestion.commands.RegisterUser;
import gov.cdc.dataingestion.commands.TokenGenerator;
import picocli.CommandLine;
import picocli.CommandLine.Command;


@Command(name = "DataIngestionCLI",
        subcommands = { RegisterUser.class, TokenGenerator.class },
        mixinStandardHelpOptions = true, version = "1.0",
        description = "Command Line Interface to connect to NBS DI Service.")
class DataIngestionCLI {

    public static void main(String[] args) {
        int exitCode = new CommandLine(new DataIngestionCLI()).execute(args);
//        System.out.println("Exiting with exit code..." + exitCode);
        System.exit(exitCode);
//        CommandLine commandLine = new CommandLine(new DataIngestionCLI());
//        commandLine.addSubcommand(new RegisterUser());
//        commandLine.addSubcommand(new TokenGenerator());
//
//        CommandLine.ParseResult parseResult = commandLine.parseArgs(args);
//
//        System.out.println("Printing subcommand..." + commandLine.getSubcommands());
//
//        if(parseResult.hasSubcommand()) {
//            CommandLine subCommand = commandLine.getSubcommands().get(0);
//            int exitCode = subCommand.execute(args);
//
//            if(exitCode == 0
//                    && !subCommand.isUsageHelpRequested()
//                    && !subCommand.isVersionHelpRequested()) {
//             while(true) {
//                 String input = System.console().readLine("> ");
//                 if(input.equalsIgnoreCase("exit")) {
//                     System.exit(exitCode);
//                 }
//
//                 int commandExitCode = commandLine.execute(input.split("\\s+"));
//                 if(commandExitCode != 0) {
//                     System.out.println("Something happened.");
//                 }
//             }
//            }
//        }
    }
}



