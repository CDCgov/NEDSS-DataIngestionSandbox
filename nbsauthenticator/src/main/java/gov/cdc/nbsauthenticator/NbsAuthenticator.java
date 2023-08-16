package gov.cdc.nbsauthenticator;

import 	org.springframework.boot.SpringApplication;
import 	org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class NbsAuthenticator {
	public static void main(String[] args) {
	    SpringApplication.run(
	    		new Class[] {
						NbsAuthenticator.class
	    		},
	    		args);
	}
}
