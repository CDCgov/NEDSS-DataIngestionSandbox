package gov.cdc.dataingestion;

import gov.cdc.dataingestion.commands.RegisterUser;
import gov.cdc.dataingestion.commands.TokenGenerator;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.MockitoAnnotations;
import picocli.CommandLine;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.io.StringWriter;
import java.util.stream.StreamSupport;

import static org.junit.jupiter.api.Assertions.*;

class DataIngestionCLITest {
    private final ByteArrayOutputStream outStream = new ByteArrayOutputStream();

    @BeforeEach
    void setUp() {
        System.setOut(new PrintStream(outStream));
    }

    @Test
    void testMainExitCodeOkArguments() {
        String[] args = { "register",  "--client-username=client", "--client-secret=secret", "--admin-user=admin", "--admin-password=password" };

        int exitCode = new CommandLine(new DataIngestionCLI()).execute(args);
        String expectedOutput = "Unauthorized. Admin username/password is incorrect.";

        assertEquals(0, exitCode);
        assertEquals(expectedOutput, outStream.toString().trim());
    }

    @Test
    void testMainExitCodeMissingArguments() {
        String[] args = { "register", "--clientSecret=secret", "--adminPassword=password" };

        int exitCode = new CommandLine(new DataIngestionCLI()).execute(args);

        assertEquals(2, exitCode);
    }

    @Test
    void testMainRegisterUserSubCommand() {
        CommandLine cmd = new CommandLine(new DataIngestionCLI());
        CommandLine subCommand = cmd.getSubcommands().get("register");

        assertNotNull(subCommand);
        assertEquals(RegisterUser.class, subCommand.getCommand().getClass());
    }

    @Test
    void testMainTokenSubCommand() {
        CommandLine cmd = new CommandLine(new DataIngestionCLI());
        CommandLine subCommand = cmd.getSubcommands().get("token");

        assertNotNull(subCommand);
        assertEquals(TokenGenerator.class, subCommand.getCommand().getClass());
    }
}