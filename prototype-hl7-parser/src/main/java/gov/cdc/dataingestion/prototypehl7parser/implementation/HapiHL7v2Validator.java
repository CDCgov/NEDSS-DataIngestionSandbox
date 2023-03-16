package gov.cdc.dataingestion.prototypehl7parser.implementation;

import ca.uhn.hl7v2.DefaultHapiContext;
import ca.uhn.hl7v2.HL7Exception;
import ca.uhn.hl7v2.HapiContext;
import ca.uhn.hl7v2.model.GenericMessage;
import ca.uhn.hl7v2.model.Message;
import ca.uhn.hl7v2.parser.*;
import ca.uhn.hl7v2.validation.impl.ValidationContextFactory;
import gov.cdc.dataingestion.prototypehl7parser.model.HL7v2Payload;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.xml.sax.InputSource;
import org.xml.sax.SAXException;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import java.io.IOException;
import java.io.StringReader;

import ca.uhn.hl7v2.util.Terser;

public class HapiHL7v2Validator {
    private HapiContext context;
    public HapiHL7v2Validator() {
        this.context = new DefaultHapiContext();
    }
    public HL7v2Payload MessageValidation(String hl7v2Message) throws HL7Exception, ParserConfigurationException, IOException, SAXException {

        // Set validation
        context.setValidationContext(ValidationContextFactory.defaultValidation());
        PipeParser parser = context.getPipeParser();

        String validatedMessageString = hl7v2Message.replaceAll("\n", "\r");

        // do parse to validate the message
        // if invalid, hl7 exception will be thrown
        Message parsedMessage = parser.parse(validatedMessageString);

        HL7v2Payload payload = new HL7v2Payload(validatedMessageString);
        payload.setHl7v2Version(parsedMessage.getVersion());

        // set context to default model
        // we will parse message into generic message
        context.setModelClassFactory(new DefaultModelClassFactory());
        Message msg = parser.parse(validatedMessageString);
        Terser terser = new Terser(msg);

        // by default from v2.1 to v2.8. MSH-9 contain message type and event trigger. Which identify the core structure of the hl7 message
        String messageType = terser.get("/MSH-9-1");
        String messageEventTrigger = terser.get("/MSH-9-2");

        payload.setHl7v2Type(messageType);
        payload.setHl7v2TriggerEvent(messageEventTrigger);
        return payload;
    }
}
