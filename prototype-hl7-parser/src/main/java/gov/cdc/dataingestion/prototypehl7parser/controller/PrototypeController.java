package gov.cdc.dataingestion.prototypehl7parser.controller;

import ca.uhn.hl7v2.HL7Exception;
import gov.cdc.dataingestion.prototypehl7parser.implementation.HapiHL7v2Parser;
import gov.cdc.dataingestion.prototypehl7parser.model.HL7v2Payload;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.io.IOException;

@RestController
@RequestMapping("/parser/")
public class PrototypeController {

    @GetMapping("/test")
    public ResponseEntity<?> helloWorld() {
        String test = "test";
        return ResponseEntity.ok(test);
    }

    @RequestMapping(value = "/hapi-parser", method = RequestMethod.POST)
    public ResponseEntity<?> parsingHLv7WithHapi(@RequestBody String payload) throws HL7Exception {

        HL7v2Payload hl7v2Payload = new HL7v2Payload(payload);
        HapiHL7v2Parser hapiHL7v2Parser = new HapiHL7v2Parser();
        // Validating HL7v2 Message
        var updatedObject = hapiHL7v2Parser.MessageValidation(hl7v2Payload.getRawHL7v2());

        // Partially parsing supported message into model for demonstration
        var parsedObject = hapiHL7v2Parser.ParsingHL7v2ToObject(updatedObject);

        return ResponseEntity.ok(parsedObject);
    }
}
