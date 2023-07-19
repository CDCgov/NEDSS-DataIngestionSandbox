package com.cdceq.duplicatesAnalyzer.processors;

import  com.cdceq.duplicatesAnalyzer.api.model.PatientDescriptor;
import  org.springframework.stereotype.Component;

import  org.apache.camel.Exchange;
import  org.apache.camel.Processor;

import 	lombok.NoArgsConstructor;

import  org.slf4j.Logger;
import  org.slf4j.LoggerFactory;

import  java.io.File;
import  java.io.FileWriter;
import  java.io.IOException;
import  java.io.PrintWriter;
import  java.util.HashMap;
import  java.util.Iterator;
import  java.util.Map;

@Component
@NoArgsConstructor
public class DuplicatesReporter implements Processor {
    private static Logger logger = LoggerFactory.getLogger(DuplicatesReporter.class);

    public void process(Exchange exchange) throws Exception {
        HashMap<Integer, PatientDescriptor> patientRecords = (HashMap<Integer, PatientDescriptor>) exchange.getIn().getBody();

        try {
            String outputFilename = exchange.getIn().getHeader("CamelFileParent")
                    + File.separator
                    + "results"
                    + File.separator
                    + exchange.getIn().getHeader("CamelFileName") + ".results";
            FileWriter fw = new FileWriter(outputFilename, true);
            PrintWriter pw = new PrintWriter(fw);

            Iterator recordsIterator = patientRecords.entrySet().iterator();
            while ( recordsIterator.hasNext() ) {
                Map.Entry mapElement = (Map.Entry) recordsIterator.next();

                PatientDescriptor pd = (PatientDescriptor) mapElement.getValue();
                pw.println(pd.formatDuplicates());
            }

            pw.flush();
            pw.close();
            fw.close();
        }
        catch(IOException e) {
            logger.error(e.toString());
        }

        exchange.getIn().setBody(patientRecords);
    }
}