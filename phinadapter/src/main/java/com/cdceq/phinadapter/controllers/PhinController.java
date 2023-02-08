package com.cdceq.phinadapter.controllers;

import	com.cdceq.phinadapter.api.model.ElrWorkerThreadUpdatePostResponse;

import  com.cdceq.phinadapter.services.NbsOdseServiceProvider;

import  io.swagger.annotations.Api;
import  io.swagger.annotations.ApiOperation;
import  io.swagger.annotations.ApiResponse;
import  io.swagger.annotations.ApiResponses;

import  org.slf4j.Logger;
import  org.slf4j.LoggerFactory;

import  org.springframework.http.HttpStatus;
import 	org.springframework.http.MediaType;
import  org.springframework.http.ResponseEntity;
import  org.springframework.web.bind.annotation.PostMapping;
import  org.springframework.web.bind.annotation.RestController;
import 	org.springframework.web.bind.annotation.RequestBody;
import 	org.springframework.beans.factory.annotation.Autowired;

import  javax.inject.Inject;

@RestController
@Api(value = "PHIN system interfacing end points", produces = MediaType.APPLICATION_XML_VALUE)
public class PhinController {
    private static Logger logger = LoggerFactory.getLogger(PhinController.class);

    @Autowired
    private NbsOdseServiceProvider serviceProvider;

    @Inject
    public PhinController() {
    }

    @PostMapping(path = "phinadapter/v1/elrwqactivator")
    @ApiOperation(value = "Update elr worker queue table for given id")
    @ApiResponses(value = {@ApiResponse(code = 200, message = "OK", response = String.class)})
    public ResponseEntity<ElrWorkerThreadUpdatePostResponse> processRequest(
            /* @RequestHeader("AuthToken") String authToken, */
            @RequestBody String payload) throws Exception {
    	/*
    	if( !isTokenValid(authToken) ) {
    		throw new Exception("Invalid auth token, please check AuthToken header value!");
    	}
    	*/

        logger.info("Processing nbs odse request for payload = {}", payload);
        int recordId = serviceProvider.processMessage(payload);

        ElrWorkerThreadUpdatePostResponse edpr = new ElrWorkerThreadUpdatePostResponse();
        edpr.setExecutionNotes("Updated row with recordId = " + recordId);

        logger.info("Processed nbs odse elrworkerthread table update request for recordId = {}", recordId);
        return new ResponseEntity<>(edpr, HttpStatus.OK);
    }

    private boolean isTokenValid(String jwtToken) throws Exception {
    	return true;
    	/*
    	if((null == jwtToken) || (jwtToken.length() <= 0)) {
    		logger.warn("Empty AuthToken header value, thus rejecting!");
    		return false;
    	}
    	*/
    }
}