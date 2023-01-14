package com.ndduc.springcomsumerdemo.repository;

import com.ndduc.springcomsumerdemo.model.Data;
import org.springframework.data.jpa.repository.JpaRepository;

public interface DataRepository extends JpaRepository<Data, Integer> {
}
