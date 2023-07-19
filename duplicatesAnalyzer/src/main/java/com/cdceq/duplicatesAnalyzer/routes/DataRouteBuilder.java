package com.cdceq.duplicatesAnalyzer.routes;

import  org.springframework.beans.factory.annotation.Autowired;
import 	org.springframework.beans.factory.annotation.Value;
import  org.springframework.stereotype.Component;

import  org.apache.camel.builder.RouteBuilder;

import	lombok.NoArgsConstructor;

import  org.slf4j.Logger;
import  org.slf4j.LoggerFactory;

import	com.cdceq.duplicatesAnalyzer.processors.CsvDataProcessor;
import	com.cdceq.duplicatesAnalyzer.processors.DuplicatesIdentifier;
import	com.cdceq.duplicatesAnalyzer.processors.DuplicatesReporter;
import	com.cdceq.duplicatesAnalyzer.processors.SummariesReporter;

@Component
@NoArgsConstructor
public class DataRouteBuilder extends RouteBuilder {
    private static final Logger logger = LoggerFactory.getLogger(DataRouteBuilder.class);

	@Value("${duplicatesAnalyzer.dataFilesDirectory}")
	private String dataFilesDirectory;

	@Autowired
	private CsvDataProcessor dataProcessor;

	@Autowired
	private DuplicatesIdentifier duplicatesIdentifier;

	@Autowired
	private DuplicatesReporter duplicatesReporter;

	@Autowired
	private SummariesReporter summariesReporter;

    @Override
    public void configure() {
		logger.info("Will process files from directory = {}", dataFilesDirectory);

		from(dataFilesDirectory)
		.routeId("FilesConsumer.Hl7.Route")
		.log("Processing inbound file ${headers.CamelFilePath}")
		.unmarshal()
		.csv()
		.process(dataProcessor)
		.log("Inbound csv data mapped to memory maps, identifying duplicates...")
		.process(duplicatesIdentifier)
		.log("Primary and default duplicates identified, generating summaries...")
		.process(summariesReporter)
		.log("Generated summaries, working on details report...")
		.process(duplicatesReporter)
		.log("Generated details report, completed processing.")
		.end();
    }
}