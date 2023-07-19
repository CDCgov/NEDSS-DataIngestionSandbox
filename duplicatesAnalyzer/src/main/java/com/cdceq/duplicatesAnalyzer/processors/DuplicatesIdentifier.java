package com.cdceq.duplicatesAnalyzer.processors;

import  com.cdceq.duplicatesAnalyzer.api.model.PatientDescriptor;
import  org.springframework.stereotype.Component;

import  org.apache.camel.Exchange;
import  org.apache.camel.Processor;

import 	lombok.NoArgsConstructor;

import  org.slf4j.Logger;
import  org.slf4j.LoggerFactory;

import  java.util.HashMap;
import  java.util.Iterator;
import  java.util.Map;

@Component
@NoArgsConstructor
public class DuplicatesIdentifier implements Processor {
    private static Logger logger = LoggerFactory.getLogger(DuplicatesIdentifier.class);

    public void process(Exchange exchange) throws Exception {
        HashMap<Integer, PatientDescriptor> patientRecords = (HashMap<Integer, PatientDescriptor>) exchange.getIn().getBody();

        Iterator recordsIterator = patientRecords.entrySet().iterator();
        while ( recordsIterator.hasNext() ) {
            Map.Entry mapElement = (Map.Entry) recordsIterator.next();

            Integer rowIdentifier = (Integer) mapElement.getKey();
            PatientDescriptor pd = (PatientDescriptor) mapElement.getValue();

            identifyDuplicates(rowIdentifier, pd, patientRecords);
        }

        exchange.getIn().setBody(patientRecords);
    }

    private void identifyDuplicates(Integer srcRow,
                                    PatientDescriptor srcPatient,
                                    HashMap<Integer, PatientDescriptor> patientRecords ) {
        Iterator recordsIterator = patientRecords.entrySet().iterator();
        while ( recordsIterator.hasNext() ) {
            Map.Entry mapElement = (Map.Entry) recordsIterator.next();

            Integer currentRow = (Integer) mapElement.getKey();
            if(srcRow.intValue() == currentRow.intValue()) {
                continue;
            }

            PatientDescriptor currentPatient = (PatientDescriptor) mapElement.getValue();

            if( srcPatient.doesMatchUsingPrimaryCriteria(currentPatient) ) {
                srcPatient.addToPrimaryCriteriaDuplicates(currentRow);
            }

            if( srcPatient.doesMatchUsingDefaultCriteria(currentPatient) ) {
                srcPatient.addToDefaultCriteriaDuplicates(currentRow);
            }
        }
    }
}