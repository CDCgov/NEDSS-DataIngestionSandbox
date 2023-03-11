package gov.cdc.dataingestion.prototypehl7parser.implementation;

import ca.uhn.hl7v2.DefaultHapiContext;
import ca.uhn.hl7v2.HL7Exception;
import ca.uhn.hl7v2.HapiContext;
import ca.uhn.hl7v2.model.Message;
import ca.uhn.hl7v2.model.v25.datatype.XPN;
import ca.uhn.hl7v2.model.v25.group.ORU_R01_PATIENT_RESULT;
import ca.uhn.hl7v2.model.v25.message.ORU_R01;
import ca.uhn.hl7v2.model.v25.segment.MSH;
import ca.uhn.hl7v2.model.v25.segment.OBR;
import ca.uhn.hl7v2.model.v25.segment.ORC;
import ca.uhn.hl7v2.model.v25.segment.PID;
import ca.uhn.hl7v2.parser.CanonicalModelClassFactory;
import ca.uhn.hl7v2.parser.PipeParser;
import ca.uhn.hl7v2.validation.impl.ValidationContextFactory;
import gov.cdc.dataingestion.prototypehl7parser.model.HL7v2Payload;

import static gov.cdc.dataingestion.prototypehl7parser.constant.HL7v2MessageSegment.*;
import static gov.cdc.dataingestion.prototypehl7parser.constant.HL7v2MessageTriggerEvent.*;
import static gov.cdc.dataingestion.prototypehl7parser.constant.HL7v2MessageType.*;
import static gov.cdc.dataingestion.prototypehl7parser.constant.HL7v2SupportVersion.*;

public class HapiHL7v2Parser {
    private HapiContext context;
    public HapiHL7v2Parser() {
        this.context = new DefaultHapiContext();
    }

    public HL7v2Payload ParsingPayloadToHL7v2(HL7v2Payload hl7v2Payload) throws HL7Exception {

        if(hl7v2Payload.getHl7v2Version().equals(SupportedHL7v2Version)) {

            /**
             * CanonicalModelClassFactory force a specific version of HL7 to be used
             * HL7 v2.x is a backward compatible standard. Choose higher version meaning we would support any of the previous version
             * */
            CanonicalModelClassFactory mcf = new CanonicalModelClassFactory(SupportedHL7v2Version);
            context.setModelClassFactory(mcf);

            /// init parser, passing factory into parser
            PipeParser parser = context.getPipeParser();

            var genericParsedMessage = parser.parse(hl7v2Payload.getRawHL7v2());
            var mshSegment = (MSH) genericParsedMessage.get("MSH");
            var messageTypeField = mshSegment.getMessageType().encode().split("\\^");
            String messageType = messageTypeField[0];
            String messageTriggerEvent = messageTypeField[1];

            hl7v2Payload.setHl7v2Type(messageType);
            hl7v2Payload.setHl7v2TriggerEvent(messageTriggerEvent);


            switch (messageType) {
                case MSG_ORU:
                    switch (messageTriggerEvent) {
                        case ORU_EVENT_RO1:
                            var parsedMessage =(ORU_R01) parser.parse(hl7v2Payload.getRawHL7v2());
                            var patientResult = (ORU_R01_PATIENT_RESULT) parsedMessage.get("PATIENT_RESULT");

                            // Extended patient name
                            var patient = patientResult.getPATIENT();
                            var pidSegment = (PID)patient.get(PID_SEGMENT);
                            var patientNameInfo = pidSegment.getPatientName();
                            if(patientNameInfo.length > 0) {
                                // Just grab first index for now
                                var pid_familyName = patientNameInfo[0].getFamilyName().encode();
                                var pid_givenName = patientNameInfo[0].getGivenName().encode();

                                hl7v2Payload.setPatientFamilyName(pid_familyName);
                                hl7v2Payload.setPatientGivenName(pid_givenName);
                            }

                            // order observation
                            var orderObservation = patientResult.getORDER_OBSERVATION();
                            var observationRequest = (OBR)orderObservation.get("OBR");
                            var obr_universalServiceIdentifier = observationRequest.getUniversalServiceIdentifier().encode();

                            var observationCommonOrder = (ORC)orderObservation.get("ORC");
                            var orc_facilityName = observationCommonOrder.getOrderingFacilityName();

                            // Further business logic can be done down here
                            break;
                        default:
                            throw new HL7Exception("Provided HL7v2 Trigger Event is not supported");
                    }
                    break;
                default:
                    throw new HL7Exception("Provided HL7v2 Message Type is not supported");
            }

          //  ca.uhn.hl7v2.model.v25.message.ORU_R01 oru_msg = (ORU_R01) parser.parse(validatedPayload);
        } else {
            throw new HL7Exception("Provided HL7v2 version is not supported");
        }

        return hl7v2Payload;
    }

    public HL7v2Payload MessageValidation(String hl7v2Message) throws HL7Exception {
        context.setValidationContext(ValidationContextFactory.defaultValidation());
        PipeParser parser = context.getPipeParser();

        String validatedMessageString = hl7v2Message.replaceAll("\n", "\r");

        Message parsedMessage = parser.parse(validatedMessageString);

        HL7v2Payload payload = new HL7v2Payload(validatedMessageString);
        payload.setHl7v2Version(parsedMessage.getVersion());

        return payload;
    }
}
