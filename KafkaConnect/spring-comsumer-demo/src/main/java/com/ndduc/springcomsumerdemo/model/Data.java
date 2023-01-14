package com.ndduc.springcomsumerdemo.model;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "consumer_test_data")
public class Data {

    public Data(Integer id, String title) {
        this.id = id;
        this.title = title;
    }

    public Data() {

    }
    @Id
    @Column(name="id")
    private Integer id;

    @Column(name="title")
    private String title;
}
