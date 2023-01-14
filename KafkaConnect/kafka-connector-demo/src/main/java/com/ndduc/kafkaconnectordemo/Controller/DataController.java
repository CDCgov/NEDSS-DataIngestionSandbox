package com.ndduc.kafkaconnectordemo.Controller;
import com.ndduc.kafkaconnectordemo.Model.Data;
import com.ndduc.kafkaconnectordemo.Model.HL7Data;
import com.ndduc.kafkaconnectordemo.Repository.DataRepository;
import com.ndduc.kafkaconnectordemo.Repository.Hl7Repository;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping(value = "/")
public class DataController {
    private final DataRepository dataRepos;

    private final Hl7Repository hl7Repository;

    public DataController(DataRepository dataRepos, Hl7Repository hl7Repository) {
        this.hl7Repository = hl7Repository;
        this.dataRepos = dataRepos;
    }


    @PostMapping(value = "/create"
    )
    public Data addNewData(@RequestBody Data data) {
        System.out.println(data.getTitle());
        return dataRepos.save(data);
    }

    @PostMapping(
            value = "/save-hl7",
            consumes = "text/plain"
    )
    public ResponseEntity<String> saveHL7File(@RequestBody String data) {
        HttpStatus httpStatus;
        HL7Data hl7Data;
        String message;
        if (data == null || data.isEmpty() || data.isBlank()) {
            httpStatus = HttpStatus.BAD_REQUEST;
            message = "Bad Data";
        } else {
            try {
                hl7Data = new HL7Data(data);
                System.out.println(data);
                hl7Repository.save(hl7Data);
                httpStatus = HttpStatus.OK;
                message = "Record " + hl7Data.getId() + " is created";
            } catch (Exception e) {
                httpStatus = HttpStatus.INTERNAL_SERVER_ERROR;
                message = e.getMessage();
            }

        }
        return new ResponseEntity<>(
                message,
                httpStatus
        );
    }


}
