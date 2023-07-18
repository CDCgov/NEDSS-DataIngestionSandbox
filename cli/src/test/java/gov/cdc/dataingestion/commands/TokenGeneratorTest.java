package gov.cdc.dataingestion.commands;

import gov.cdc.dataingestion.model.AuthModel;
import gov.cdc.dataingestion.util.AuthUtil;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.MockitoAnnotations;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class TokenGeneratorTest {
    private final ByteArrayOutputStream outStream = new ByteArrayOutputStream();
    private final ByteArrayOutputStream errStream = new ByteArrayOutputStream();
    @Mock
    AuthUtil authUtilMock;

    private TokenGenerator tokenGenerator;

    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
        System.setOut(new PrintStream(outStream));
        System.setErr(new PrintStream(errStream));
        tokenGenerator = new TokenGenerator();
        tokenGenerator.authUtil = authUtilMock;
        tokenGenerator.authModel = new AuthModel();
        tokenGenerator.authModel.setServiceEndpoint("https://dataingestion.datateam-cdc-nbs.eqsandbox.com/token");
    }

    @AfterEach
    void tearDown() {
        Mockito.reset(authUtilMock);
    }

    @Test
    void testRunSuccess() {
        String adminUser = "admin";
        char[] adminPassword = "adminPassword".toCharArray();
        String apiResponse = "Dummy_Token";

        when(authUtilMock.getResponseFromDIService(any(AuthModel.class))).thenReturn(apiResponse);

        tokenGenerator.adminUser = adminUser;
        tokenGenerator.adminPassword = adminPassword;
        tokenGenerator.run();

        verify(authUtilMock).getResponseFromDIService(tokenGenerator.authModel);
        assertEquals(apiResponse, outStream.toString().trim());
    }

    @Test
    void testRunAdminUnauthorized() {
        String adminUser = "notAdmin";
        char[] adminPassword = "notAdminPassword".toCharArray();
        String apiResponse = "Unauthorized. Admin username/password is incorrect.";

        when(authUtilMock.getResponseFromDIService(any(AuthModel.class))).thenReturn(apiResponse);

        tokenGenerator.adminUser = adminUser;
        tokenGenerator.adminPassword = adminPassword;
        tokenGenerator.run();

        verify(authUtilMock).getResponseFromDIService(tokenGenerator.authModel);
        assertEquals(apiResponse, outStream.toString().trim());
    }

    @Test
    void testRunEmptyAdminUsernameOrPassword() {
        String adminUser = "";
        char[] adminPassword = "adminPassword".toCharArray();
        String expectedOutput = "Admin username or password is empty.";

        tokenGenerator.adminUser = adminUser;
        tokenGenerator.adminPassword = adminPassword;
        tokenGenerator.run();

        verify(authUtilMock, never()).getResponseFromDIService(any(AuthModel.class));
        assertEquals(expectedOutput, errStream.toString().trim());
    }

    @Test
    void testRunNullAdminUsernameOrPassword() {
        String adminUser = "admin";
        char[] adminPassword = null;
        String expectedOutput = "Admin username or password is null.";

        tokenGenerator.adminUser = adminUser;
        tokenGenerator.adminPassword = adminPassword;
        tokenGenerator.run();

        verify(authUtilMock, never()).getResponseFromDIService(any(AuthModel.class));
        assertEquals(expectedOutput, errStream.toString().trim());
    }
}