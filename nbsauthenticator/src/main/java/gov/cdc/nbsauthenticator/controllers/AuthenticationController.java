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
import  org.springframework.web.bind.annotation.GetMapping;
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

        int authUserId = authenticator.signon(user, password);
        if(authUserId < 0) {
            return new ResponseEntity<>("Not authorized", HttpStatus.FORBIDDEN);
        }

        String remoteAddr = request.getRemoteAddr();;
        String token = authenticator.createToken(remoteAddr, authUserId, user);

        JSONObject reply = new JSONObject();
        reply.put("token", token);

        return new ResponseEntity<>(reply.toString(), HttpStatus.OK);
    }

    @GetMapping(path = "nbsauth/token")
    @ApiOperation(value = "Generate new token")
    @ApiResponses(value = {@ApiResponse(code = 200, message = "OK", response = String.class)})
    public ResponseEntity<String> getToken(@RequestHeader(value="Auth-Token") String currentToken, HttpServletRequest request) throws Exception {
        if(null == authenticator) {
            authenticator = authenticatorFactory.getAuthenticator();
        }

        String remoteAddr = request.getRemoteAddr();
        String token = authenticator.generateToken(remoteAddr, currentToken);

        JSONObject reply = new JSONObject();
        reply.put("token", token);

        return new ResponseEntity<>(reply.toString(), HttpStatus.OK);
    }
}
