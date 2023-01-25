package com.cdceq.nbsadapter.controllers;

import	com.cdceq.nbsadapter.api.model.ElrDataPostResponse;
import  com.cdceq.nbsadapter.services.ElrDataServiceProvider;

import  io.swagger.annotations.Api;
import  io.swagger.annotations.ApiOperation;
import  io.swagger.annotations.ApiResponse;
import  io.swagger.annotations.ApiResponses;

import  org.slf4j.Logger;
import  org.slf4j.LoggerFactory;

import  org.springframework.beans.factory.annotation.Autowired;
import 	org.springframework.beans.factory.annotation.Value;

import  org.springframework.http.HttpStatus;
import 	org.springframework.http.MediaType;
import  org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import  org.springframework.web.bind.annotation.PostMapping;
import  org.springframework.web.bind.annotation.RestController;
//import  org.springframework.web.bind.annotation.RequestHeader;
import 	org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;

import	java.util.List;

@RestController
@Api(value = "NBS adapter end points", produces = MediaType.APPLICATION_XML_VALUE)
public class ReportStreamController {
    private static Logger logger = LoggerFactory.getLogger(ReportStreamController.class);  
    
    @Autowired 
    private ElrDataServiceProvider serviceProvider;

    public ReportStreamController() {
    }
    
    @GetMapping(path = "/elrs")
    @ApiOperation(value = "Get all elrs")
    @ApiResponses(value = {@ApiResponse(code = 200, message = "OK", response = String.class)})
    public ResponseEntity<String> getAll() throws Exception {
    	serviceProvider.findAll();
    	String outMsg = "Check logs";
    	logger.info(outMsg);
        return new ResponseEntity<>(outMsg, HttpStatus.OK);
    }    
    
    @PostMapping(path = "/elr")
    @ApiOperation(value = "Post ELR data")
    @ApiResponses(value = {@ApiResponse(code = 200, message = "OK", response = String.class)})
    public ResponseEntity<ElrDataPostResponse> processElrData(/* @RequestHeader("AuthToken") String authToken, */
    												@RequestBody String xmlPayload) throws Exception {
    	/*
    	if( !isTokenValid(authToken) ) {
    		throw new Exception("Invalid auth token, please check AuthToken header value!");
    	}
    	*/
    	
    	System.out.println("xmlPayload: " + xmlPayload);
    	
    	serviceProvider.saveMessage(xmlPayload);
    	
    	
    	ElrDataPostResponse edpr = new ElrDataPostResponse();
    	edpr.setExecutionNotes("Saved data to the store");
    	
    	logger.info("Processed elr post request");
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