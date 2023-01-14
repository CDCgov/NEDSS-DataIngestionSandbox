package com.ndduc.kafkaconnectordemo.Model;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

import java.util.Date;
import java.util.UUID;


@Document(collection = "data")
public class HL7Data {
    public HL7Data(String object) {
        this.setId();
        this.setObject(object);
        this.setTimestamp(new Date());
    }

    @Id
    private String id;
    private String object;
    private Date timestamp;


    public String getId() {
        return id;
    }

    public void setId() {
        this.id =  UUID.randomUUID().toString();
    }

    public String getObject() {
        return object;
    }

    public void setObject(String object) {
        this.object = object;
    }

    public Date getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(Date timestamp) {
        this.timestamp = timestamp;
    }
}
