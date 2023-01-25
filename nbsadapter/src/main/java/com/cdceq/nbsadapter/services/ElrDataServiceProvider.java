package com.cdceq.nbsadapter.services;

import	com.cdceq.nbsadapter.persistance.model.EntityNbsInterface;
import 	com.cdceq.nbsadapter.persistance.NbsInterfaceRepository;

import 	org.springframework.beans.factory.annotation.Autowired;
import 	org.springframework.stereotype.Service;

import  org.slf4j.Logger;
import  org.slf4j.LoggerFactory;

import	lombok.NoArgsConstructor;

import	java.util.GregorianCalendar;
import	java.sql.Timestamp;

@Service
@NoArgsConstructor
public class ElrDataServiceProvider {
	private static Logger LOG = LoggerFactory.getLogger(ElrDataServiceProvider.class);
	
	private static String IMPEXP_CD_E = "E";
	private static String STATUS_UNPROCESSED = "UNPROCESSED";
	private static String SYSTEM_NAME_NBS = "NBS";
	private static String DOCUMENT_TYPE_CODE = "11648804";
	
    @Autowired
    private NbsInterfaceRepository nbsInterfaceRepo;
    
    public boolean saveMessage(String msgXml) {
    	EntityNbsInterface msg = new EntityNbsInterface();
    	
    	msg.setPayload(msgXml);
    	msg.setImpExpIndCd(IMPEXP_CD_E);
    	msg.setRecordStatusCd(STATUS_UNPROCESSED);
    	
    	GregorianCalendar currentTimestamp = new GregorianCalendar();
    	Timestamp recordTimestamp = new Timestamp(currentTimestamp.getTimeInMillis());

    	msg.setRecordStatusTime(recordTimestamp);
    	msg.setAddTime(recordTimestamp);
    	
    	msg.setSystemNm(SYSTEM_NAME_NBS);
    	msg.setDocTypeCd(DOCUMENT_TYPE_CODE);
    	msg.setOriginalPayload(null);
    	msg.setOriginalDocTypeCd(null);
    	msg.setFillerOrderNbr(null);
    	msg.setLabClia(null);
    	msg.setSpecimenCollDate(null);
    	msg.setOrderTestCode(null);
    	msg.setObservationUid(null);
    	
    	nbsInterfaceRepo.save(msg);

    	return true;
    }
    
    public void findAll() {
        Iterable<EntityNbsInterface> itemsIterator = nbsInterfaceRepo.findAll();
        
        for(EntityNbsInterface item : itemsIterator) {
        	LOG.info(item.toString());
        }
    }
}