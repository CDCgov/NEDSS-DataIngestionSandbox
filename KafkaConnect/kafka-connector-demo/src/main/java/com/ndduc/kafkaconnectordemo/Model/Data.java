package com.ndduc.kafkaconnectordemo.Model;

import org.springframework.data.annotation.Id;

import java.util.Date;

public class Data {

    public Data(String id, String title) {
        this.id = id;
        this.title = title;
    }

    @Id
    private String id;
    private String title;
    private Date timeStamp = new Date();

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public Date getTimeStamp() {
        return timeStamp;
    }

    public void setTimeStamp(Date timeStamp) {
        this.timeStamp = timeStamp;
    }


    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }
}
