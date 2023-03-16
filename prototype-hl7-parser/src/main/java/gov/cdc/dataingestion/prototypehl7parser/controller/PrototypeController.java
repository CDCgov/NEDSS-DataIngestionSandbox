package gov.cdc.dataingestion.prototypehl7parser.controller;

import ca.uhn.hl7v2.HL7Exception;
import gov.cdc.dataingestion.prototypehl7parser.implementation.HL7v2ToFhir;
import gov.cdc.dataingestion.prototypehl7parser.implementation.HapiHL7v2Parser;
import gov.cdc.dataingestion.prototypehl7parser.implementation.HapiHL7v2Validator;
import gov.cdc.dataingestion.prototypehl7parser.model.HL7v2Payload;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.xml.sax.SAXException;

import javax.xml.parsers.ParserConfigurationException;
import java.io.IOException;

@RestController
@RequestMapping("/parser/")
public class PrototypeController {

    @RequestMapping(value = "/hapi-parser", method = RequestMethod.POST)
    public ResponseEntity<?> parsingHLv7WithHapi(@RequestBody String payload) throws HL7Exception, ParserConfigurationException, IOException, SAXException {

        HL7v2Payload hl7v2Payload = new HL7v2Payload(payload);
        HapiHL7v2Parser hapiHL7v2Parser = new HapiHL7v2Parser();
        HapiHL7v2Validator hapiHL7v2Validator = new HapiHL7v2Validator();
        // Validating HL7v2 Message
        var updatedObject = hapiHL7v2Validator.MessageValidation(hl7v2Payload.getRawHL7v2());

        // Partially parsing supported message into model for demonstration
        var parsedObject = hapiHL7v2Parser.ParsingPayloadToHL7v2(updatedObject);

        return ResponseEntity.ok(parsedObject);
    }


    @RequestMapping(value = "/convert/hl7tofhir", method = RequestMethod.POST)
    public ResponseEntity<?> convertHL7v2ToFHIR(@RequestBody String payload) {

        HL7v2ToFhir hl7v2ToFhir = new HL7v2ToFhir();
        var output = hl7v2ToFhir.ConvertHL7v2ToFhir(payload);

        return ResponseEntity.ok(output);
    }
}
