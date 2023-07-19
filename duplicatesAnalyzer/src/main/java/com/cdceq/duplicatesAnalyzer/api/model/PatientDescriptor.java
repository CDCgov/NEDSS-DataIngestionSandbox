package com.cdceq.duplicatesAnalyzer.api.model;

import  java.util.List;
import  java.util.ArrayList;

import	lombok.Getter;
import	lombok.Setter;
import	lombok.NoArgsConstructor;

import  org.apache.commons.lang3.StringUtils;

@Getter
@Setter
@NoArgsConstructor
public class PatientDescriptor {
    public static int COLUMN_ID = 0;
    public static int COLUMN_BIRTHDATE = 1;
    public static int COLUMN_DEATHDATE = 2;
    public static int COLUMN_SSN = 3;
    public static int COLUMN_DRIVERSLICENSE = 4;
    public static int COLUMN_PASSPORT = 5;
    public static int COLUMN_PREFIX = 6;
    public static int COLUMN_FIRST_NAME = 7;
    public static int COLUMN_LAST_NAME = 8;
    public static int COLUMN_SUFFIX = 9;
    public static int COLUMN_MARTIAL_STATUS = 10;
    public static int COLUMN_RACE = 11;
    public static int COLUMN_ETHINICITY = 12;
    public static int COLUMN_GENDER = 13;
    public static int COLUMN_BIRTH_PLACE = 14;
    public static int COLUMN_ADDRESS = 15;
    public static int COLUMN_CITY = 16;
    public static int COLUMN_STATE = 17;
    public static int COLUMN_COUNTY = 18;
    public static int COLUMN_FIPS = 19;
    public static int COLUMN_ZIP = 20;

    private String id;
    private String idType = "default";
    private String assigningAuthority = "default";
    private String birthDate;
    private String deathDate;
    private String ssn;
    private String driversLicense;
    private String passport;
    private String prefix;
    private String firstName;
    private String lastName;
    private String suffix;
    private String maritalStatus;
    private String race;
    private String ethinicity;
    private String gender;
    private String birthPlace;
    private String address;
    private String city;
    private String state;
    private String county;
    private String fips;
    private String zip;

    private Integer rowIdentifier;
    private ArrayList<Integer> primaryCriteriaDuplicates = new ArrayList<>();
    private ArrayList<Integer> defaultCriteriaDuplicates = new ArrayList<>();

    public static PatientDescriptor createPatient(Integer rowIdentifier, List<String> dataRecord) {
        if( StringUtils.isEmpty(dataRecord.get(COLUMN_ID)) ) {
            return null;
        }

        PatientDescriptor pd = new PatientDescriptor();

        pd.rowIdentifier = rowIdentifier;

        pd.id = dataRecord.get(COLUMN_ID);

        if( !StringUtils.isEmpty(dataRecord.get(COLUMN_BIRTHDATE)) ) {
            pd.birthDate = dataRecord.get(COLUMN_BIRTHDATE);
        }

        if( !StringUtils.isEmpty(dataRecord.get(COLUMN_SSN)) ) {
            pd.ssn = dataRecord.get(COLUMN_SSN);
        }

        if( !StringUtils.isEmpty(dataRecord.get(COLUMN_DRIVERSLICENSE)) ) {
            pd.driversLicense = dataRecord.get(COLUMN_DRIVERSLICENSE);
        }

        if( !StringUtils.isEmpty(dataRecord.get(COLUMN_PASSPORT)) ) {
            pd.passport = dataRecord.get(COLUMN_PASSPORT);
        }

        if( !StringUtils.isEmpty(dataRecord.get(COLUMN_PREFIX)) ) {
            pd.prefix = dataRecord.get(COLUMN_PREFIX);
        }

        if( !StringUtils.isEmpty(dataRecord.get(COLUMN_FIRST_NAME)) ) {
            pd.firstName = dataRecord.get(COLUMN_FIRST_NAME);
        }

        if( !StringUtils.isEmpty(dataRecord.get(COLUMN_FIRST_NAME)) ) {
            pd.firstName = dataRecord.get(COLUMN_FIRST_NAME);
        }

        if( !StringUtils.isEmpty(dataRecord.get(COLUMN_LAST_NAME)) ) {
            pd.lastName = dataRecord.get(COLUMN_LAST_NAME);
        }

        if( !StringUtils.isEmpty(dataRecord.get(COLUMN_SUFFIX)) ) {
            pd.suffix = dataRecord.get(COLUMN_SUFFIX);
        }

        if( !StringUtils.isEmpty(dataRecord.get(COLUMN_MARTIAL_STATUS)) ) {
            pd.maritalStatus = dataRecord.get(COLUMN_MARTIAL_STATUS);
        }

        if( !StringUtils.isEmpty(dataRecord.get(COLUMN_RACE)) ) {
            pd.race = dataRecord.get(COLUMN_RACE);
        }

        if( !StringUtils.isEmpty(dataRecord.get(COLUMN_ETHINICITY)) ) {
            pd.ethinicity = dataRecord.get(COLUMN_ETHINICITY);
        }

        if( !StringUtils.isEmpty(dataRecord.get(COLUMN_GENDER)) ) {
            pd.gender = dataRecord.get(COLUMN_GENDER);
        }

        if( !StringUtils.isEmpty(dataRecord.get(COLUMN_BIRTH_PLACE)) ) {
            pd.birthPlace = dataRecord.get(COLUMN_BIRTH_PLACE);
        }

        if( !StringUtils.isEmpty(dataRecord.get(COLUMN_ADDRESS)) ) {
            pd.address = dataRecord.get(COLUMN_ADDRESS);
        }

        if( !StringUtils.isEmpty(dataRecord.get(COLUMN_CITY)) ) {
            pd.city = dataRecord.get(COLUMN_CITY);
        }

        if( !StringUtils.isEmpty(dataRecord.get(COLUMN_STATE)) ) {
            pd.state = dataRecord.get(COLUMN_STATE);
        }

        if( !StringUtils.isEmpty(dataRecord.get(COLUMN_COUNTY)) ) {
            pd.county = dataRecord.get(COLUMN_COUNTY);
        }

        if( !StringUtils.isEmpty(dataRecord.get(COLUMN_COUNTY)) ) {
            pd.county = dataRecord.get(COLUMN_COUNTY);
        }

        if( !StringUtils.isEmpty(dataRecord.get(COLUMN_FIPS)) ) {
            pd.fips = dataRecord.get(COLUMN_FIPS);
        }

        if( !StringUtils.isEmpty(dataRecord.get(COLUMN_ZIP)) ) {
            pd.zip = dataRecord.get(COLUMN_ZIP);
        }

        return pd;
    }

    private String buildBasicInformation() {
        StringBuilder sb = new StringBuilder();

        sb.append(rowIdentifier);
        sb.append(" | ");
        sb.append(id);
        sb.append(" | ");
        sb.append(firstName);
        sb.append(" | ");
        sb.append(lastName);

        return sb.toString();
    }

    public String formatDuplicates() {
        StringBuilder sb = new StringBuilder();

        sb.append(buildBasicInformation());

        if((primaryCriteriaDuplicates.size() == 0) && (defaultCriteriaDuplicates.size() == 0)) {
            sb.append(" | ");
            sb.append("[]");
            sb.append(" | ");
            sb.append("[]");
            return sb.toString();
        }

        sb.append(" ");
        sb.append("[");
        sb.append(getPrimaryCriteriaDuplicates());
        sb.append("]");
        sb.append(" | ");
        sb.append("{");
        sb.append(getDefaultCriteriaDuplicates());
        sb.append("}");

        return sb.toString();
    }

    public void addToPrimaryCriteriaDuplicates(Integer duplicateRowNumber) {
        synchronized (primaryCriteriaDuplicates) {
            primaryCriteriaDuplicates.add(duplicateRowNumber);
        }
    }

    public void addToDefaultCriteriaDuplicates(Integer duplicateRowNumber) {
        synchronized (defaultCriteriaDuplicates) {
            defaultCriteriaDuplicates.add(duplicateRowNumber);
        }
    }

    public boolean doesHavePrimaryCriteriaDuplicates() {
        return primaryCriteriaDuplicates.size() > 0;
    }

    /*
    public int primaryCriteriaDuplicatesCount() {
        return primaryCriteriaDuplicates.size();
    }

    public int defaultCriteriaDuplicatesCount() {
        return primaryCriteriaDuplicates.size();
    }
    */

    public String getPrimaryCriteriaDuplicates() {
        if( !doesHavePrimaryCriteriaDuplicates() ) return "";

        ArrayList<Integer> clonedList = null;
        StringBuilder sb = new StringBuilder();

        synchronized (primaryCriteriaDuplicates) {
            clonedList = (ArrayList<Integer>) primaryCriteriaDuplicates.clone();
        }

        return buildBufferFromList(clonedList);
    }

    public boolean doesHaveDefaultCriteriaDuplicates() {
        return defaultCriteriaDuplicates.size() > 0;
    }

    public String getDefaultCriteriaDuplicates() {
        if( !doesHaveDefaultCriteriaDuplicates() ) return "";

        ArrayList<Integer> clonedList = null;
        StringBuilder sb = new StringBuilder();

        synchronized (defaultCriteriaDuplicates) {
            clonedList = (ArrayList<Integer>) defaultCriteriaDuplicates.clone();
        }

        return buildBufferFromList(clonedList);
    }

    private String buildBufferFromList(ArrayList<Integer> listOfItems) {
        StringBuilder sb = new StringBuilder();

        for(Integer duplicate : listOfItems) {
            if(sb.length() > 0) {
                sb.append(", ");
            }

            sb.append(duplicate);
        }

        return sb.toString();
    }

    public boolean doesMatchUsingPrimaryCriteria(PatientDescriptor other) {
        if(StringUtils.isEmpty(this.id) ||
           StringUtils.isEmpty(this.idType)  ||
           StringUtils.isEmpty(this.assigningAuthority) ||
           StringUtils.isEmpty((this.firstName)) ||
           StringUtils.isEmpty((this.firstName))) return false;

        return (this.id.equals(other.id) &&
            this.idType.equals(other.idType) &&
            this.assigningAuthority.equals(other.assigningAuthority) &&
            this.firstName.equals(other.firstName) &&
            this.lastName.equals(other.lastName));
    }

    public boolean doesMatchUsingDefaultCriteria(PatientDescriptor other) {
        if(StringUtils.isEmpty(this.firstName) ||
           StringUtils.isEmpty(this.lastName)  ||
           StringUtils.isEmpty(this.birthDate) ||
           StringUtils.isEmpty((this.gender))) return false;

        return (this.firstName.equals(other.firstName) &&
                this.lastName.equals(other.lastName) &&
                this.birthDate.equals(other.birthDate) &&
                this.gender.equals(other.gender) );
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();

        sb.append(id);
        sb.append(":");
        sb.append(firstName);
        sb.append(":");
        sb.append(lastName);

        return sb.toString();
    }
}

