package com.ndduc.kafkaconnectordemo.Kafka.Consumer;

import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Component;

import java.time.Duration;

@Component
public class KafkaConsumer {
    @Autowired
    private KafkaTemplate<String, String> kafkaTemplate;

    public ConsumerRecord<String, String> consumerMessageOnDemand(String topic, int partition, int offset, Duration pollTimeout) {
        ConsumerRecord<String, String> record = kafkaTemplate.receive(topic, partition, offset, pollTimeout);
        System.out.println(record.value());
        return record;
    }
}
