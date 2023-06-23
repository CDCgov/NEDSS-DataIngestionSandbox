package gov.cdc.dataingestion.commands;

import gov.cdc.dataingestion.util.AuthUtil;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;

import java.io.*;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.when;

class RegisterUserTest {
    private RegisterUser registerUser;
    private ByteArrayInputStream inputStream;
    private ByteArrayOutputStream outputStream;


    @BeforeEach
    void setUp() {
        registerUser = new RegisterUser();
        outputStream = new ByteArrayOutputStream();
        System.setOut(new PrintStream(outputStream));
    }

    @AfterEach
    void tearDown() {
    }

    @Test
    void testRun_SuccessfulRegistration() {
        String username = "testUser";
        char[] password = "testPassword".toCharArray();

        AuthUtil authUtilMock = Mockito.mock(AuthUtil.class);
        when(authUtilMock.getString(username, password, "dummy_endpoint")).thenReturn("CREATED");

        registerUser.run();

        String expectedOutput = "User onboarded successfully.";
        assertEquals(expectedOutput, outputStream.toString().trim());
    }

    @Test
    void testRun_UnSuccessfulRegistration() {
//        registerUser.username = "existingUser";
//        registerUser.password = "testPassword".toCharArray();

        String username = "testUser";
        char[] password = "testPassword".toCharArray();

        AuthUtil authUtilMock = Mockito.mock(AuthUtil.class);
        when(authUtilMock.getString(username, password, "dummy_endpoint")).thenReturn("NOT_ACCEPTABLE");

        registerUser.run();

        String expectedOutput = "Username already exists. Please choose a unique client username.";
        assertEquals(expectedOutput, outputStream.toString().trim());
    }
}