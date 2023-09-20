package gov.cdc.nbsauthenticator.services.authimpls;

import	lombok.NoArgsConstructor;
import	lombok.Getter;
import	lombok.Setter;

import  org.slf4j.Logger;
import  org.slf4j.LoggerFactory;
import  org.springframework.stereotype.Component;

@NoArgsConstructor
@Getter
@Setter
@Component
public class OktaAuthAuthenticator extends CommonAuthenticator {
    private static Logger logger = LoggerFactory.getLogger(OktaAuthAuthenticator.class);

    @Override
    public String[] signon(String remoteAddr, String user, String userPassword) throws Exception {
        logger.info("OktaAuthAuthenticator::signon");
        return super.signon(remoteAddr, user, userPassword);
    }
}
