package com.ndduc.springcomsumerdemo.model;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

import java.util.Date;

@Getter
@Setter
@Entity
@Table(name = "consumer_hl7_data")
public class HL7Data {

    public HL7Data() {

    }

    public HL7Data(String id, String object) {
        this.id = id;
        this.object = object;
        this.timeStamp = new Date();
    }
    @Id
    private String id;

    @Column(columnDefinition = "TEXT")
    private String object;


    @Column(name = "patient_first_name")
    private String patientFirstName;

    @Column(name = "patient_last_name")
    private String patientLastName;

    @Column(name="time_stamp")
    private Date timeStamp;
}
