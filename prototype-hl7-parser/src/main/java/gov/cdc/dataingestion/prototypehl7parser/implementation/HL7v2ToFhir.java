package gov.cdc.dataingestion.prototypehl7parser.implementation;

import io.github.linuxforhealth.hl7.HL7ToFHIRConverter;

public class HL7v2ToFhir {
    private HL7ToFHIRConverter converter;
    public HL7v2ToFhir() {
        this.converter = new HL7ToFHIRConverter();
    }
    public String ConvertHL7v2ToFhir(String hl7Payload) {
        // converted string is in JSON format
        String output = this.converter.convert(hl7Payload);
        return output;
    }
}
