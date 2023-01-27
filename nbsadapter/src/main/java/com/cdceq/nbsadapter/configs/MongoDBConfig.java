package com.cdceq.nbsadapter.configs;

import  org.springframework.data.mongodb.config.AbstractMongoClientConfiguration;
import  org.springframework.data.mongodb.repository.config.EnableMongoRepositories;
import  org.springframework.data.mongodb.MongoDatabaseFactory;
import  org.springframework.context.annotation.Configuration;
import  org.springframework.context.annotation.DependsOn;
import  org.springframework.beans.factory.annotation.Value;

import  com.mongodb.ConnectionString;
import  com.mongodb.MongoClientSettings;
import  com.mongodb.client.MongoClient;
import  com.mongodb.client.MongoClients;

import  org.slf4j.Logger;
import  org.slf4j.LoggerFactory;

import  java.io.File;
import  java.util.Collection;
import  java.util.Collections;

import	com.vault.utils.VaultValuesResolver;

@Configuration
@EnableMongoRepositories(basePackages = "com.cdceq.nbsadapter.persistance")
public class MongoDBConfig extends AbstractMongoClientConfiguration {
    private static Logger logger = LoggerFactory.getLogger(MongoDBConfig.class);

    @Value("${mongo.dbname}")
    private String vaultMongoDbName;

    @Value("${mongo.url}")
    private String vaultMongoUrl;

    @DependsOn(value = {
            "vaultValuesResolver"
    })
    @Override
    public MongoDatabaseFactory mongoDbFactory() {
        return super.mongoDbFactory();
    }

    @Override
    protected String getDatabaseName() {
        return VaultValuesResolver.getVaultKeyValue(vaultMongoDbName);
    }

    @Override
    public MongoClient mongoClient() {
        String strConnectionString  = VaultValuesResolver.getVaultKeyValue(vaultMongoUrl)
                                    + File.separator
                                    + getDatabaseName();
        final ConnectionString connectionString = new ConnectionString(strConnectionString);
        final MongoClientSettings mongoClientSettings = MongoClientSettings.builder()
                        .applyConnectionString(connectionString)
                        .build();
        return MongoClients.create(mongoClientSettings);
    }

    @Override
    public Collection<String> getMappingBasePackages() {
        return Collections.singleton("com.cdceq.nbsadapter.persistance");
    }
}