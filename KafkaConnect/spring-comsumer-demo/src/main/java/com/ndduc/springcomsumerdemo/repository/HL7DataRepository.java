package com.ndduc.springcomsumerdemo.repository;

import com.ndduc.springcomsumerdemo.model.Data;
import com.ndduc.springcomsumerdemo.model.HL7Data;
import org.springframework.data.jpa.repository.JpaRepository;

public interface HL7DataRepository  extends JpaRepository<HL7Data, String> {
}
