package com.ndduc.kafkaconnectordemo.Repository;

import com.ndduc.kafkaconnectordemo.Model.Data;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface DataRepository extends MongoRepository<Data, String> {
}
