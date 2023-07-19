package com.cdceq.duplicatesAnalyzer.processors;

import  com.cdceq.duplicatesAnalyzer.api.model.PatientDescriptor;
import  org.springframework.stereotype.Component;

import  org.apache.camel.Exchange;
import  org.apache.camel.Processor;

import 	lombok.NoArgsConstructor;

import  org.slf4j.Logger;
import  org.slf4j.LoggerFactory;

import  java.util.List;
import  java.util.HashMap;
import  java.util.Iterator;
import  java.util.Map;

@Component
@NoArgsConstructor
public class CsvDataProcessor implements Processor {
    private static Logger logger = LoggerFactory.getLogger(CsvDataProcessor.class);

    private HashMap<Integer, PatientDescriptor> patientRecords = new HashMap<>();

    public void process(Exchange exchange) throws Exception {
        List<List<String>> data = (List<List<String>>) exchange.getIn().getBody();
        int row = 0;
        for (List<String> line : data) {
            row++;
            if(row == 1) {
                continue;   // ignore header
            }

            Integer rowIdentifier = new Integer(row);
            PatientDescriptor pd = PatientDescriptor.createPatient(rowIdentifier, line);

            patientRecords.put(rowIdentifier, pd);
        }

        exchange.getIn().setBody(patientRecords);
    }
}