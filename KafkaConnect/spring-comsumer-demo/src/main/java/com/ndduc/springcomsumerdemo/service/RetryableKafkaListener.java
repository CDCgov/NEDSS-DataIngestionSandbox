package com.ndduc.springcomsumerdemo.service;

import com.google.gson.JsonParser;
import com.ndduc.springcomsumerdemo.bl.Hl7HapiBL;
import com.ndduc.springcomsumerdemo.helper.MessageHelper;
import com.ndduc.springcomsumerdemo.model.Data;
import com.ndduc.springcomsumerdemo.model.HL7Data;
import com.ndduc.springcomsumerdemo.model.HL7ParseModel;
import com.ndduc.springcomsumerdemo.repository.DataRepository;
import com.ndduc.springcomsumerdemo.repository.HL7DataRepository;
import lombok.extern.slf4j.Slf4j;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.common.errors.SerializationException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.annotation.DltHandler;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.annotation.RetryableTopic;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.retrytopic.TopicSuffixingStrategy;
import org.springframework.kafka.support.KafkaHeaders;
import org.springframework.kafka.support.serializer.DeserializationException;
import org.springframework.messaging.handler.annotation.Header;
import org.springframework.retry.annotation.Backoff;
import org.springframework.stereotype.Component;

@Component
@Slf4j
public class RetryableKafkaListener {
    @Autowired
    private DataRepository dataRepository;

    @Autowired
    private HL7DataRepository hl7DataRepository;

    @RetryableTopic(
            attempts = "5",
            // retry topic name, such as topic-retry-1, topic-retry-2, etc
            topicSuffixingStrategy = TopicSuffixingStrategy.SUFFIX_WITH_INDEX_VALUE,
            // time to wait before attempting to retry
            backoff = @Backoff(delay = 1000, multiplier = 2.0),
            // if these exceptions occur, skip retry then push message to DLQ
            exclude = {SerializationException.class, DeserializationException.class}

    )

    @KafkaListener(id = "${spring.kafka.consumer.group-id}", topics = "${topic}")
    public void handleMessage(ConsumerRecord<String, String> consumerRecord, String message, @Header(KafkaHeaders.RECEIVED_TOPIC) String topic) {
        log.info("Received message: {} from topic: {}", message, topic);
        try {
            String id = MessageHelper.extractId(message);
            String originalClass = MessageHelper.extractOriginalClass(message);
            if (originalClass.equalsIgnoreCase("com.ndduc.kafkaconnectordemo.Model.HL7Data")) {
                String object = MessageHelper.extractValue(message, "object");
                Hl7HapiBL  hapiBL = new Hl7HapiBL();
                HL7ParseModel parseModel = hapiBL.simpleHL7PatientNameValidation(object);
                HL7Data hl7Data = new HL7Data(id, object);
                hl7Data.setPatientFirstName(parseModel.getPatientFirstName());
                hl7Data.setPatientLastName(parseModel.getPatientLastName());
                hl7DataRepository.save(hl7Data);
            } else {
                String title = MessageHelper.extractValue(message, "title");
                Data data = new Data(Integer.valueOf(id), title);
                dataRepository.save(data);
            }
        } catch (Exception e) {
            System.out.println(e.getMessage());
            // run time error then -- do retry
            throw new RuntimeException(e.getMessage());
        }
    }

    @DltHandler
    public void handleDlt(String message, @Header(KafkaHeaders.RECEIVED_TOPIC) String topic) {
        // Once in DLQ -- we can save message in actual db for further analyze
        log.info("Message: {} handled by dlq topic: {}", message, topic);
    }



}