package com.cdceq.nbsadapter.routes;

import  org.springframework.beans.factory.annotation.Autowired;
import 	org.springframework.beans.factory.annotation.Value;
import  org.springframework.stereotype.Component;

import  org.apache.camel.builder.RouteBuilder;

import	lombok.NoArgsConstructor;

import  org.slf4j.Logger;
import  org.slf4j.LoggerFactory;

import  com.cdceq.nbsadapter.exceptions.ValidationException;
import	com.cdceq.nbsadapter.processors.Hl7ToXmlTransformer;
import	com.cdceq.nbsadapter.processors.XmlDataPersister;
@Component
@NoArgsConstructor
public class LegacyHl7RouteBuilder extends RouteBuilder {
    private static final Logger logger = LoggerFactory.getLogger(LegacyHl7RouteBuilder.class);

	@Value("${report-stream.hl7-files-dir-url}")
	private String hl7FilesDirectoryUrl;

	@Value("${kafka.outbound.hl7-messages-endpoint}")
	private String 	hl7MsgsEndpoint;

	@Value("${kafka.outbound.xml-messages-endpoint}")
	private String 	xmlMsgsEndpoint;

	@Autowired
	private Hl7ToXmlTransformer hl7ToXmlTransformer;

	@Autowired
	private XmlDataPersister xmlDataPersister;

    @Override
    public void configure() {
		logger.info("Report stream hl7 files directory = {}", hl7FilesDirectoryUrl);

        onException(ValidationException.class)
        .log("Observed validation exception")
        .markRollbackOnly()
        .useOriginalMessage()
        .logStackTrace(true)        
        .end();

        onException(Exception.class)
        .log("Observed exception")
        .markRollbackOnly()
        .useOriginalMessage()
        .logStackTrace(true)
        .end();

		from(hl7FilesDirectoryUrl)
		.routeId("Legacy.Hl7.FilesConsumer.Route")
		.to("seda:hl7_file_processing_route", "seda:kafka_hl7_producer_route")
		.end();

		from("seda:kafka_hl7_producer_route")
		.to(hl7MsgsEndpoint)
		.log("Dispatched to kafka hl7 messages topic")
		.end();

		from("seda:hl7_file_processing_route")
		.log("Processing file ${headers.CamelFileName} from file system")
		.process(hl7ToXmlTransformer)
		.log("Xml: ${body}")
		.to("seda:xml_persist_to_db_route", "seda:kafka_xml_producer_route")
		.end();

		from("seda:xml_persist_to_db_route")
		.process(xmlDataPersister)
		.log("Processed file ${headers.CamelFileName}, persisted as xml message to sql server database")
		.end();

		from("seda:kafka_xml_producer_route")
		.to(xmlMsgsEndpoint)
		.log("Dispatched to kafka xml messages topic")
		.end();
    }
}