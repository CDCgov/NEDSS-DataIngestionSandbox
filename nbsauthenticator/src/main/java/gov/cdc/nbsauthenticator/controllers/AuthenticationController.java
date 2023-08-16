package gov.cdc.nbsauthenticator.controllers;

//import  com.cdceq.jwtgenerator.services.TokenGenerator;

import  io.swagger.annotations.Api;
import  io.swagger.annotations.ApiOperation;
import  io.swagger.annotations.ApiResponse;
import  io.swagger.annotations.ApiResponses;

import  org.springframework.http.HttpStatus;
import 	org.springframework.http.MediaType;
import  org.springframework.http.ResponseEntity;
import  org.springframework.web.bind.annotation.GetMapping;
import  org.springframework.web.bind.annotation.RestController;
import 	org.springframework.web.bind.annotation.RequestHeader;
import 	org.springframework.beans.factory.annotation.Autowired;
import  org.springframework.beans.factory.annotation.Value;

import  javax.servlet.http.HttpServletRequest;

import  org.json.JSONObject;
import  org.jasypt.encryption.pbe.StandardPBEStringEncryptor;

import  javax.inject.Inject;

import  org.slf4j.Logger;
import  org.slf4j.LoggerFactory;

@RestController
@Api(value = "NBS Authentication Controller", produces = MediaType.APPLICATION_XML_VALUE)
public class AuthenticationController {
    private static Logger logger = LoggerFactory.getLogger(AuthenticationController.class);

    //@Autowired
    //private HttpServletRequest request;

    //@Autowired
    //private TokenGenerator tokenGenerator;

    //@Value("${jwt.seed}")
    //private String jwtSeed;

    private StandardPBEStringEncryptor decryptor = new StandardPBEStringEncryptor();
    private boolean bInitialized = false;

    @Inject
    public AuthenticationController() {
    }

    private void init() {
    }

    @GetMapping(path = "nbsauth/token")
    @ApiOperation(value = "Generate new token")
    @ApiResponses(value = {@ApiResponse(code = 200, message = "OK", response = String.class)})
    public ResponseEntity<String> getToken() throws Exception {
        init();

        //String remoteAddr = request.getRemoteAddr();
        //String token = tokenGenerator.generateToken(appPassPhrase, remoteAddr);

        JSONObject reply = new JSONObject();
        reply.put("token", "Work-in-pogress");

        return new ResponseEntity<>(reply.toString(), HttpStatus.OK);
    }
}
