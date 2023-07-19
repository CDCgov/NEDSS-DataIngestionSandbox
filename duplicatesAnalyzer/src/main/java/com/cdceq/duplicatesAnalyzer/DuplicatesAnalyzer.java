package com.cdceq.duplicatesAnalyzer;

import 	org.springframework.boot.SpringApplication;
import 	org.springframework.boot.autoconfigure.SpringBootApplication;
@SpringBootApplication
public class DuplicatesAnalyzer {
	public static void main(String[] args) {
	    SpringApplication.run(
	    		new Class[] {
						DuplicatesAnalyzer.class
	    		},
	    		args);
	}
}
