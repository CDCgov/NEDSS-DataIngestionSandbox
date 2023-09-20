package gov.cdc.nbsauthenticator.controllers;

import  gov.cdc.nbsauthenticator.services.AuthenticatorFactory;
import  gov.cdc.nbsauthenticator.services.IAuthenticator;

import  io.swagger.annotations.Api;
import  io.swagger.annotations.ApiOperation;
import  io.swagger.annotations.ApiResponse;
import  io.swagger.annotations.ApiResponses;

import  org.springframework.http.HttpStatus;
import 	org.springframework.http.MediaType;
import  org.springframework.http.ResponseEntity;
import  org.springframework.web.bind.annotation.PostMapping;
import  org.springframework.web.bind.annotation.RestController;
import  org.springframework.web.bind.annotation.RequestParam;
import  org.springframework.web.bind.annotation.RequestHeader;
import 	org.springframework.beans.factory.annotation.Autowired;

import  jakarta.servlet.http.HttpServletRequest;

import  org.json.JSONObject;
import  org.jasypt.encryption.pbe.StandardPBEStringEncryptor;

import  javax.inject.Inject;

import  org.slf4j.Logger;
import  org.slf4j.LoggerFactory;
import  java.util.HashMap;
import  java.util.Map;

@RestController
@Api(value = "NBS Authentication Controller", produces = MediaType.APPLICATION_XML_VALUE)
public class AuthenticationController {
    private static Logger logger = LoggerFactory.getLogger(AuthenticationController.class);

    @Autowired
    private AuthenticatorFactory authenticatorFactory;


    private StandardPBEStringEncryptor decryptor = new StandardPBEStringEncryptor();
    private boolean bInitialized = false;

    private IAuthenticator  authenticator;

    @Inject
    public AuthenticationController() {
    }

    @PostMapping(path = "nbsauth/signon")
    @ApiOperation(value = "Generate new token")
    @ApiResponses(value = {@ApiResponse(code = 200, message = "OK", response = String.class)})
    public ResponseEntity<String> signon(@RequestParam(required = true) String user,
                                         @RequestParam(required = true) String password,
                                         HttpServletRequest request) throws Exception {

        if(null == authenticator) {
            authenticator = authenticatorFactory.getAuthenticator();
        }

        String remoteAddr = request.getRemoteAddr();;

        String tokens[] = authenticator.signon(remoteAddr, user, password);
        if((null == tokens) || (null == tokens[1])) {
            return new ResponseEntity<>("Not authorized", HttpStatus.FORBIDDEN);
        }

        JSONObject reply = new JSONObject();
        reply.put("token", tokens[0]);
        reply.put("refreshToken", tokens[1]);

        logger.info("Completed signon, returning token[0] = {}, token[1]", tokens[0], tokens[1]);

        return new ResponseEntity<>(reply.toString(), HttpStatus.OK);
    }

    @PostMapping(path = "nbsauth/roles")
    @ApiOperation(value = "Return decoded roles as json")
    @ApiResponses(value = {@ApiResponse(code = 200, message = "OK", response = String.class)})
    public ResponseEntity<String> getRoles(@RequestHeader(value="Auth-Token") String currentToken, HttpServletRequest request) throws Exception {
        if(null == authenticator) {
            authenticator = authenticatorFactory.getAuthenticator();
        }

        String remoteAddr = request.getRemoteAddr();
        String rolesStr = authenticator.getRoles(remoteAddr, currentToken);

        JSONObject reply = new JSONObject();
        reply.put("roles", rolesStr);

        logger.info("Returning obtained roles");
        return new ResponseEntity<>(reply.toString(), HttpStatus.OK);
    }

    @PostMapping(path = "nbsauth/token")
    @ApiOperation(value = "Generate new token")
    @ApiResponses(value = {@ApiResponse(code = 200, message = "OK", response = String.class)})
    public ResponseEntity<String> getToken(@RequestHeader(value="Auth-Token") String currentToken, HttpServletRequest request) throws Exception {
        if(null == authenticator) {
            authenticator = authenticatorFactory.getAuthenticator();
        }

        String remoteAddr = request.getRemoteAddr();
        String[] tokens = authenticator.generateToken(remoteAddr, currentToken);

        JSONObject reply = new JSONObject();
        reply.put("token", tokens[0]);
        reply.put("refreshToken", tokens[1]);

        logger.info("Completed refresh token, returning token[0] = {}, token[1]", tokens[0], tokens[1]);

        return new ResponseEntity<>(reply.toString(), HttpStatus.OK);
    }
}
