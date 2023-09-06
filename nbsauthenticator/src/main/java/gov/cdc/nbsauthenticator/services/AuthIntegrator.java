package gov.cdc.nbsauthenticator.services;

import  org.springframework.stereotype.Component;
import  org.springframework.context.ApplicationListener;
import  org.springframework.boot.context.event.ApplicationReadyEvent;

import  org.slf4j.Logger;
import  org.slf4j.LoggerFactory;

@Component
public class AuthIntegrator implements ApplicationListener<ApplicationReadyEvent> {
    private static Logger logger = LoggerFactory.getLogger(AuthIntegrator.class);

    @Override
    public void onApplicationEvent(final ApplicationReadyEvent event) {
        logger.info("Hello Alpha");
        return;
    }
}

