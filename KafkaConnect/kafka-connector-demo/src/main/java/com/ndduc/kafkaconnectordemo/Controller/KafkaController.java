package com.ndduc.kafkaconnectordemo.Controller;
import com.ndduc.kafkaconnectordemo.Kafka.Consumer.KafkaConsumer;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.time.Duration;

@RestController
@RequestMapping(value="/kafka")
public class KafkaController {

    @Autowired
    KafkaConsumer kafkaConsumer;

    @PostMapping(value = "/replay-dlq"
    )
    public void addNewData() {
        // kafkaConsumer.consumer();
        Duration duration = Duration.ofSeconds(1);
        kafkaConsumer.consumerMessageOnDemand("dlq.mongo.data", 0, 9, duration);
    }
}
