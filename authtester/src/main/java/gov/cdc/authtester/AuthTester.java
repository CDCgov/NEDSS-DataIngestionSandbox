package gov.cdc.authtester;

import 	org.springframework.boot.SpringApplication;
import 	org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class AuthTester {
	public static void main(String[] args) {
	    SpringApplication.run(
	    		new Class[] {
				AuthTester.class
	    		},
	    		args);
	}
}
