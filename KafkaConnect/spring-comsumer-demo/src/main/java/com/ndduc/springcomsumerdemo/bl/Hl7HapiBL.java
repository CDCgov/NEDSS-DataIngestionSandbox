package com.ndduc.springcomsumerdemo.bl;

import ca.uhn.hl7v2.DefaultHapiContext;
import ca.uhn.hl7v2.HL7Exception;
import ca.uhn.hl7v2.HapiContext;
import ca.uhn.hl7v2.model.v25.datatype.XPN;
import ca.uhn.hl7v2.model.v25.message.ORU_R01;
import ca.uhn.hl7v2.parser.*;
import com.ndduc.springcomsumerdemo.model.HL7ParseModel;

import java.util.regex.Pattern;

public class Hl7HapiBL {
    private HapiContext context = new DefaultHapiContext();
    private CanonicalModelClassFactory mcf = new CanonicalModelClassFactory("2.5");
    PipeParser parser;

    public Hl7HapiBL() {
        this.context.setModelClassFactory(mcf);
        this.parser = this.context.getPipeParser();
    }

    public HL7ParseModel simpleHL7PatientNameValidation(String message) {

        if(!Pattern.compile("\r").matcher(message).find()) {
            message = message.replaceAll("\n", "\r\n");
        }
        HL7ParseModel model = new HL7ParseModel();
        try {
            // parsing v23 to v25
            ORU_R01 msg = (ORU_R01) parser.parse(message);
            XPN[] patient = msg.getPATIENT_RESULT().getPATIENT().getPID().getPatientName();
            if(patient.length > 0) {
                model.setPatientFirstName(patient[0].getGivenName().toString());
                model.setPatientLastName(patient[0].getFamilyName().getFn1_Surname().toString());
            }
        } catch (HL7Exception e) {
            throw new RuntimeException(e.getMessage());
        }
        return model;
    }
}
