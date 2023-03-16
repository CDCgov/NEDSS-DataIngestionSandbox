package gov.cdc.dataingestion.prototypehl7parser.implementation;

import ca.uhn.hl7v2.DefaultHapiContext;
import ca.uhn.hl7v2.HL7Exception;
import ca.uhn.hl7v2.HapiContext;
import ca.uhn.hl7v2.model.v251.group.ORU_R01_PATIENT_RESULT;
import ca.uhn.hl7v2.model.v251.message.ORU_R01;
import ca.uhn.hl7v2.model.v251.segment.OBR;
import ca.uhn.hl7v2.model.v251.segment.ORC;
import ca.uhn.hl7v2.model.v251.segment.PID;
import ca.uhn.hl7v2.parser.CanonicalModelClassFactory;
import ca.uhn.hl7v2.parser.PipeParser;
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

            /**
             * CanonicalModelClassFactory force a specific version of HL7 to be used
             * HL7 v2.x is a backward compatible standard. Choose higher version meaning we would support any of the previous version
             * */
            CanonicalModelClassFactory mcf = new CanonicalModelClassFactory(HL7v251);
            context.setModelClassFactory(mcf);

            /// init parser, passing factory into parser
            PipeParser parser = context.getPipeParser();

            switch (hl7v2Payload.getHl7v2Type()) {
                case MSG_ORU:
                    switch (hl7v2Payload.getHl7v2TriggerEvent()) {
                        case ORU_EVENT_RO1:
                            ORU_R01_PATIENT_RESULT patientResult;
                            if (hl7v2Payload.getHl7v2Version().equals(HL7v251) ||
                                    hl7v2Payload.getHl7v2Version().equals(HL7v25) ||
                                    hl7v2Payload.getHl7v2Version().equals(HL7v23)) {

                                // provided structure is 2.5.1. Hence it support converting any older structure to newest provided one
                                var parsedMessage =(ORU_R01) parser.parse(hl7v2Payload.getRawHL7v2());
                                patientResult = (ORU_R01_PATIENT_RESULT) parsedMessage.get("PATIENT_RESULT");
                            }
                            else {
                                throw new HL7Exception("Provided HL7v2 Version is not supported\t\t" + hl7v2Payload.getHl7v2Version());
                            }

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
                            throw new HL7Exception("Provided HL7v2 Trigger Event is not supported\t\t" + hl7v2Payload.getHl7v2TriggerEvent());
                    }
                    break;
                default:
                    throw new HL7Exception("Provided HL7v2 Message Type is not supported\t\t" + hl7v2Payload.getHl7v2Type());
            }

        return hl7v2Payload;
    }


}
