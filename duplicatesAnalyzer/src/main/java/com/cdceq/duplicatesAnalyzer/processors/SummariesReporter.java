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
import  java.util.Date;

import  java.io.File;
import  java.io.FileWriter;
import  java.io.PrintWriter;
import  java.io.IOException;

@Component
@NoArgsConstructor
public class SummariesReporter implements Processor {
    private static Logger logger = LoggerFactory.getLogger(SummariesReporter.class);

    public void process(Exchange exchange) throws Exception {
        StringBuilder sb = new StringBuilder();
        int primaryDuplicatesCount = 0;
        int defaultDuplicatesCount = 0;
        HashMap<Integer, PatientDescriptor> patientRecords = (HashMap<Integer, PatientDescriptor>) exchange.getIn().getBody();

        Iterator recordsIterator = patientRecords.entrySet().iterator();
        while ( recordsIterator.hasNext() ) {
            Map.Entry mapElement = (Map.Entry) recordsIterator.next();

            PatientDescriptor pd = (PatientDescriptor) mapElement.getValue();
            if( pd.doesHavePrimaryCriteriaDuplicates() ) {
                primaryDuplicatesCount++;
            }

            if( pd.doesHaveDefaultCriteriaDuplicates() ) {
                defaultDuplicatesCount++;
            }
        }

        sb.append("Date and time of analysis - ");
        sb.append(new Date());
        sb.append("\n");
        
        sb.append("Input file = ");
        sb.append(exchange.getIn().getHeader("CamelFilePath"));
        //sb.append(exchange.getIn().getHeader("CamelFileName"));
        //sb.append(" file path - ");
        //sb.append(exchange.getIn().getHeader("CamelFileParent"));
        sb.append("\n");

        sb.append("Record count in file (excluding header record) = ");
        sb.append(patientRecords.size());
        sb.append("\n");

        sb.append("Primary criteria matched records count = ");
        sb.append(primaryDuplicatesCount);
        sb.append("\n");

        sb.append("Default criteria matched records count = ");
        sb.append(defaultDuplicatesCount);
        sb.append("\n");

        try {
            String outputFilename = exchange.getIn().getHeader("CamelFileParent")
                                  + File.separator
                                  + "results"
                                  + File.separator
                                  + exchange.getIn().getHeader("CamelFileName") + ".results";
            FileWriter fw = new FileWriter(outputFilename, true);
            PrintWriter pw = new PrintWriter(fw);
            pw.println(sb.toString());
            pw.flush();
            pw.close();
            fw.close();
        }
        catch(IOException e) {
            logger.info(sb.toString());
        }

        exchange.getIn().setBody(patientRecords);
    }
}