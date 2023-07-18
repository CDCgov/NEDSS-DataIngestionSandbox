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
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;
import static org.mockito.Mockito.never;

class InjectHL7Test {
    private final ByteArrayOutputStream outStream = new ByteArrayOutputStream();
    private final ByteArrayOutputStream errStream = new ByteArrayOutputStream();
    @Mock
    private AuthUtil authUtilMock;
    private InjectHL7 injectHL7;

    private String hl7FilePath = "path/to/hl7-input.hl7";

    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
        System.setOut(new PrintStream(outStream));
        System.setErr(new PrintStream(errStream));
        injectHL7 = new InjectHL7();
        injectHL7.authUtil = authUtilMock;
        injectHL7.authModel = new AuthModel();
        injectHL7.authModel.setServiceEndpoint("https://dataingestion.datateam-cdc-nbs.eqsandbox.com/api/reports");
    }

    @AfterEach
    void tearDown() {
        Mockito.reset(authUtilMock);
    }

    @Test
    void testRunSuccessfulInjection() throws IOException {
        String adminUser = "adminUser";
        char[] adminPassword = "adminPassword".toCharArray();
        String apiResponse = "Dummy_UUID";

        when(authUtilMock.getResponseFromDIService(any(AuthModel.class))).thenReturn(apiResponse);
        File tempHL7File = getFile();

        injectHL7.hl7FilePath = tempHL7File.getAbsolutePath();
        injectHL7.adminUser = adminUser;
        injectHL7.adminPassword = adminPassword;

        injectHL7.run();

        ArgumentCaptor<AuthModel> authModelCaptor = ArgumentCaptor.forClass(AuthModel.class);
        verify(authUtilMock).getResponseFromDIService(authModelCaptor.capture());

        String expectedOutput = "Dummy_UUID";
        assertEquals("adminUser", authModelCaptor.getValue().getAdminUser());
        assertArrayEquals("adminPassword".toCharArray(), authModelCaptor.getValue().getAdminPassword());
//        assertEquals("MSH|^~\\&|SIMHOSP|SFAC|RAPP|RFAC|20200508130643||ADT^A01|5|T|2.3|||AL||44|ASCII\n" +
//                "EVN|A01|20200508130643|||C006^Wolf^Kathy^^^Dr^^^DRNBR^PRSNL^^^ORGDR|\n" +
//                "PID|1|2590157853^^^SIMULATOR MRN^MRN|2590157853^^^SIMULATOR MRN^MRN~2478684691^^^NHSNBR^NHSNMBR||Esterkin^AKI Scenario 6^^^Miss^^CURRENT||19890118000000|F|||170 Juice Place^^London^^RW21 6KC^GBR^HOME||020 5368 1665^HOME|||||||||R^Other - Chinese^^^||||||||\n" +
//                "PD1|||FAMILY PRACTICE^^12345|\n" +
//                "PV1|1|I|RenalWard^MainRoom^Bed 1^Simulated Hospital^^BED^Main Building^5|28b|||C006^Wolf^Kathy^^^Dr^^^DRNBR^PRSNL^^^ORGDR|||MED|||||||||6145914547062969032^^^^visitid||||||||||||||||||||||ARRIVED|||20200508130643||", authModelCaptor.getValue().getRequestBody());
        assertEquals(expectedOutput, outStream.toString().trim());

        assertTrue(tempHL7File.delete());
    }

    @Test
    void testRunInvalidPath() {
        String adminUser = "adminUser";
        char[] adminPassword = "adminPassword".toCharArray();

        injectHL7.hl7FilePath = "invalid-path/to/hl7-input.hl7";
        injectHL7.adminUser = adminUser;
        injectHL7.adminPassword = adminPassword;

        assertThrows(RuntimeException.class, injectHL7::run);
    }

    @Test
    void testRunAdminUnauthorized() throws IOException {
        String adminUser = "notAdmin";
        char[] adminPassword = "notAdminPassword".toCharArray();
        String apiResponse = "Unauthorized. Admin username/password is incorrect.";

        when(authUtilMock.getResponseFromDIService(any(AuthModel.class))).thenReturn(apiResponse);
        File tempHL7File = getFile();

        injectHL7.adminUser = adminUser;
        injectHL7.adminPassword = adminPassword;
        injectHL7.hl7FilePath = tempHL7File.getAbsolutePath();
        injectHL7.run();

        verify(authUtilMock).getResponseFromDIService(injectHL7.authModel);
        assertEquals(apiResponse, outStream.toString().trim());
    }

    @Test
    void testRunEmptyAdminUsernameOrPassword() {
        String adminUser = "";
        char[] adminPassword = "adminPassword".toCharArray();
        String expectedOutput = "Admin username or password is empty.";

        injectHL7.adminUser = adminUser;
        injectHL7.adminPassword = adminPassword;
        injectHL7.hl7FilePath = hl7FilePath;
        injectHL7.run();

        verify(authUtilMock, never()).getResponseFromDIService(any(AuthModel.class));
        assertEquals(expectedOutput, errStream.toString().trim());
    }

    @Test
    void testRunNullAdminUsernameOrPassword() {
        String adminUser = "admin";
        char[] adminPassword = null;
        String expectedOutput = "One or more inputs are null.";

        injectHL7.adminUser = adminUser;
        injectHL7.adminPassword = adminPassword;
        injectHL7.hl7FilePath = hl7FilePath;
        injectHL7.run();

        verify(authUtilMock, never()).getResponseFromDIService(any(AuthModel.class));
        assertEquals(expectedOutput, errStream.toString().trim());
    }

    @Test
    void testRunAllEmptyInputs() {
        injectHL7.hl7FilePath = null;
        injectHL7.adminUser = null;
        injectHL7.adminPassword = null;

        injectHL7.run();

        String expectedOutput = "One or more inputs are null.";
        assertEquals(expectedOutput, errStream.toString().trim());
        verifyNoInteractions(authUtilMock);
    }

    private static File getFile() throws IOException {
        File tempHL7File = File.createTempFile("test-hl7-input", ".hl7");

        try (FileWriter writer = new FileWriter(tempHL7File)) {
            writer.write("MSH|^~\\&|SIMHOSP|SFAC|RAPP|RFAC|20200508130643||ADT^A01|5|T|2.3|||AL||44|ASCII\n" +
                    "EVN|A01|20200508130643|||C006^Wolf^Kathy^^^Dr^^^DRNBR^PRSNL^^^ORGDR|\n" +
                    "PID|1|2590157853^^^SIMULATOR MRN^MRN|2590157853^^^SIMULATOR MRN^MRN~2478684691^^^NHSNBR^NHSNMBR||Esterkin^AKI Scenario 6^^^Miss^^CURRENT||19890118000000|F|||170 Juice Place^^London^^RW21 6KC^GBR^HOME||020 5368 1665^HOME|||||||||R^Other - Chinese^^^||||||||\n" +
                    "PD1|||FAMILY PRACTICE^^12345|\n" +
                    "PV1|1|I|RenalWard^MainRoom^Bed 1^Simulated Dummy Hospital^^BED^Main Building^5|28b|||C006^Wolf^Kathy^^^Dr^^^DRNBR^PRSNL^^^ORGDR|||MED|||||||||6145914547062969032^^^^visitid||||||||||||||||||||||ARRIVED|||20200508130643||");
        }
        return tempHL7File;
    }
}