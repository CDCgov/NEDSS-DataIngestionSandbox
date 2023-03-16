package gov.cdc.dataingestion.prototypehl7parser.model;

public class HL7v2Payload {
    private String rawHL7v2;
    private String hl7v2Version;
    private String hl7v2Type;
    private String hl7v2TriggerEvent;

    private String patientFamilyName;
    private String patientGivenName;

    public HL7v2Payload() {};
    public HL7v2Payload(String rawHL7v2) {
        this.rawHL7v2 = rawHL7v2;
    }

    public String getRawHL7v2() {
        return rawHL7v2;
    }

    public void setRawHL7v2(String rawHL7v2) {
        this.rawHL7v2 = rawHL7v2;
    }

    public String getHl7v2Version() {
        return hl7v2Version;
    }

    public void setHl7v2Version(String hl7v2Version) {
        this.hl7v2Version = hl7v2Version;
    }

    public String getHl7v2Type() {
        return hl7v2Type;
    }

    public void setHl7v2Type(String hl7v2Type) {
        this.hl7v2Type = hl7v2Type;
    }

    public String getHl7v2TriggerEvent() {
        return hl7v2TriggerEvent;
    }

    public void setHl7v2TriggerEvent(String hl7v2TriggerEvent) {
        this.hl7v2TriggerEvent = hl7v2TriggerEvent;
    }

    public String getPatientFamilyName() {
        return patientFamilyName;
    }

    public void setPatientFamilyName(String patientFamilyName) {
        this.patientFamilyName = patientFamilyName;
    }

    public String getPatientGivenName() {
        return patientGivenName;
    }

    public void setPatientGivenName(String patientGivenName) {
        this.patientGivenName = patientGivenName;
    }
}
