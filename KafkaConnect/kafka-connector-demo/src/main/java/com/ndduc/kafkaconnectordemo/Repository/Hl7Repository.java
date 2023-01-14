package com.ndduc.kafkaconnectordemo.Repository;

import com.ndduc.kafkaconnectordemo.Model.HL7Data;
import org.apache.kafka.common.Uuid;
import org.springframework.data.mongodb.repository.MongoRepository;

public interface Hl7Repository extends MongoRepository<HL7Data, String> {
}
