package gov.cdc.dataingestion.commands;

import gov.cdc.dataingestion.model.AuthModel;
import gov.cdc.dataingestion.util.AuthUtil;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.ArgumentCaptor;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.MockitoAnnotations;

import java.io.*;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

class RegisterUserTest {
    private final ByteArrayOutputStream outStream = new ByteArrayOutputStream();
    private final ByteArrayOutputStream errStream = new ByteArrayOutputStream();
    @Mock
    private AuthUtil authUtilMock;
    private RegisterUser registerUser;
    // private String serviceEndpoint = "";



    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
        System.setOut(new PrintStream(outStream));
        System.setErr(new PrintStream(errStream));
        registerUser = new RegisterUser();
        registerUser.authUtil = authUtilMock;
        registerUser.authModel = new AuthModel();
        registerUser.authModel.setServiceEndpoint("https://dataingestion.datateam-cdc-nbs.eqsandbox.com/registration?username=testUser&password=testPassword");
    }

    @AfterEach
    void tearDown() {
        Mockito.reset(authUtilMock);
    }

    @Test
    void testRunSuccessfulRegistration() {
        registerUser.username = "testUser";
        registerUser.password = "testPassword".toCharArray();
        registerUser.adminUser = "adminUser";
        registerUser.adminPassword = "adminPassword".toCharArray();

        when(authUtilMock.getResponseFromDIService(any(AuthModel.class))).thenReturn("CREATED");

        registerUser.run();

        ArgumentCaptor<AuthModel> authModelCaptor = ArgumentCaptor.forClass(AuthModel.class);
        verify(authUtilMock).getResponseFromDIService(authModelCaptor.capture());

        String expectedOutput = "User onboarded successfully.";
        assertEquals("adminUser", authModelCaptor.getValue().getAdminUser());
        assertArrayEquals("adminPassword".toCharArray(), authModelCaptor.getValue().getAdminPassword());
        assertEquals(expectedOutput, outStream.toString().trim());
    }

    @Test
    void testRunUsernameAlreadyExists() {
        registerUser.username = "testUser";
        registerUser.password = "testPassword".toCharArray();
        registerUser.adminUser = "adminUser";
        registerUser.adminPassword = "adminPassword".toCharArray();

        when(authUtilMock.getResponseFromDIService(any(AuthModel.class))).thenReturn("NOT_ACCEPTABLE");

        registerUser.run();

        ArgumentCaptor<AuthModel> authModelCaptor = ArgumentCaptor.forClass(AuthModel.class);
        verify(authUtilMock).getResponseFromDIService(authModelCaptor.capture());

        String expectedOutput = "Username already exists. Please choose a unique client username.";
        assertEquals("adminUser", authModelCaptor.getValue().getAdminUser());
        assertArrayEquals("adminPassword".toCharArray(), authModelCaptor.getValue().getAdminPassword());
        assertEquals(expectedOutput, outStream.toString().trim());
    }

    @Test
    void testRunAdminUnauthorized() {
        registerUser.username = "testUser";
        registerUser.password = "testPassword".toCharArray();
        registerUser.adminUser = "notAdminUser";
        registerUser.adminPassword = "notAdminPassword".toCharArray();

        when(authUtilMock.getResponseFromDIService(any(AuthModel.class))).thenReturn("Unauthorized. Admin username/password is incorrect.");

        registerUser.run();

        ArgumentCaptor<AuthModel> authModelCaptor = ArgumentCaptor.forClass(AuthModel.class);
        verify(authUtilMock).getResponseFromDIService(authModelCaptor.capture());

        String expectedOutput = "Unauthorized. Admin username/password is incorrect.";
        assertEquals("notAdminUser", authModelCaptor.getValue().getAdminUser());
        assertArrayEquals("notAdminPassword".toCharArray(), authModelCaptor.getValue().getAdminPassword());
        assertEquals(expectedOutput, outStream.toString().trim());
    }

    @Test
    void testRunNullResponse() {
        registerUser.username = "testUser";
        registerUser.password = "testPassword".toCharArray();
        registerUser.adminUser = "notAdminUser";
        registerUser.adminPassword = "notAdminPassword".toCharArray();

        when(authUtilMock.getResponseFromDIService(any(AuthModel.class))).thenReturn(null);

        registerUser.run();

        ArgumentCaptor<AuthModel> authModelCaptor = ArgumentCaptor.forClass(AuthModel.class);
        verify(authUtilMock).getResponseFromDIService(authModelCaptor.capture());

        String expectedOutput = "Something went wrong with API. Response came back as null.";
        assertEquals("notAdminUser", authModelCaptor.getValue().getAdminUser());
        assertArrayEquals("notAdminPassword".toCharArray(), authModelCaptor.getValue().getAdminPassword());
        assertEquals(expectedOutput, errStream.toString().trim());
    }

    @Test
    void testRunException() {
        registerUser.username = "testUser";
        registerUser.password = "testPassword".toCharArray();
        registerUser.adminUser = "notAdminUser";
        registerUser.adminPassword = "notAdminPassword".toCharArray();

        when(authUtilMock.getResponseFromDIService(any(AuthModel.class))).thenThrow(new RuntimeException("An exception occurred."));

        assertThrows(RuntimeException.class, registerUser::run);
    }

    @Test
    void testRunAllEmptyInputs() {
        registerUser.username = "";
        registerUser.password = "".toCharArray();
        registerUser.adminUser = "";
        registerUser.adminPassword = "".toCharArray();

        registerUser.run();

        String expectedOutput = "One or more inputs are empty.";
        assertEquals(expectedOutput, errStream.toString().trim());
        verifyNoInteractions(authUtilMock);
    }

    @Test
    void testRunSomeEmptyInputs() {
        registerUser.username = "testUser";
        registerUser.password = "".toCharArray();
        registerUser.adminUser = "";
        registerUser.adminPassword = "adminPassword".toCharArray();

        registerUser.run();

        String expectedOutput = "One or more inputs are empty.";
        assertEquals(expectedOutput, errStream.toString().trim());
        verifyNoInteractions(authUtilMock);
    }

    @Test
    void testRunAllNullInputs() {
        registerUser.username = null;
        registerUser.password = null;
        registerUser.adminUser = null;
        registerUser.adminPassword = null;

        registerUser.run();

        String expectedOutput = "One or more inputs are null.";
        assertEquals(expectedOutput, errStream.toString().trim());
        verifyNoInteractions(authUtilMock);
    }

    @Test
    void testRunSomeNullInputs() {
        registerUser.username = null;
        registerUser.password = "testPassword".toCharArray();
        registerUser.adminUser = "adminUser";
        registerUser.adminPassword = null;

        registerUser.run();

        String expectedOutput = "One or more inputs are null.";
        assertEquals(expectedOutput, errStream.toString().trim());
        verifyNoInteractions(authUtilMock);
    }
}