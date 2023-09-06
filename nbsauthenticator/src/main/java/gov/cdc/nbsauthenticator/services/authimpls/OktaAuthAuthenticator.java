package gov.cdc.nbsauthenticator.services.authimpls;

import	lombok.NoArgsConstructor;
import	lombok.Getter;
import	lombok.Setter;

import  org.slf4j.Logger;
import  org.slf4j.LoggerFactory;

@NoArgsConstructor
@Getter
@Setter
public class OktaAuthAuthenticator extends CommonAuthenticator {
    private static Logger logger = LoggerFactory.getLogger(OktaAuthAuthenticator.class);

    @Override
    public int signon(String user, String userPassword) {
        logger.info("OktaAuthAuthenticator::signon");
        return 0;
    }
}
