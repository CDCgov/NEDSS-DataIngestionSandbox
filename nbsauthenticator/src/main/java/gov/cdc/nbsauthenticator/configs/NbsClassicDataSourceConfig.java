package gov.cdc.nbsauthenticator.configs;

import  org.slf4j.Logger;
import  org.slf4j.LoggerFactory;
import  org.springframework.beans.factory.annotation.Value;
import  org.springframework.boot.jdbc.DataSourceBuilder;
import  org.springframework.context.annotation.Bean;

import  org.springframework.beans.factory.annotation.Qualifier;
import  org.springframework.context.annotation.Configuration;
import  org.springframework.data.jpa.repository.config.EnableJpaRepositories;
import  org.springframework.orm.jpa.LocalContainerEntityManagerFactoryBean;
import  org.springframework.boot.orm.jpa.EntityManagerFactoryBuilder;
import  org.springframework.transaction.PlatformTransactionManager;
import  org.springframework.orm.jpa.JpaTransactionManager;
import  org.springframework.orm.jpa.vendor.HibernateJpaVendorAdapter;

import  javax.sql.DataSource;
import  jakarta.persistence.EntityManagerFactory;
import  org.springframework.transaction.annotation.EnableTransactionManagement;

import  java.util.HashMap;

@Configuration
@EnableTransactionManagement
@EnableJpaRepositories(
        entityManagerFactoryRef = "authEntityManagerFactory",
        transactionManagerRef = "authTransactionManager",
        basePackages = {
                "gov.cdc.nbsauthenticator.repositories"
        }
)
public class NbsClassicDataSourceConfig {
    private static final Logger logger = LoggerFactory.getLogger(NbsClassicDataSourceConfig.class);

    @Value("${spring.datasource.nbsclassic.driverClassName}")
    private String driverClassName;

    @Value("${spring.datasource.nbsclassic.url}")
    private String dbUrl;

    @Value("${spring.datasource.nbsclassic.username}")
    private String dbUser;

    @Value("${spring.datasource.nbsclassic.password}")
    private String dbUserPassword;

    @Bean()
    public DataSource dataSource() {
        DataSourceBuilder dataSourceBuilder = DataSourceBuilder.create();

        dataSourceBuilder.driverClassName(driverClassName);
        dataSourceBuilder.url(dbUrl);
        dataSourceBuilder.username(dbUser);
        dataSourceBuilder.password(dbUserPassword);

        return dataSourceBuilder.build();
    }

    @Bean
    public EntityManagerFactoryBuilder authEntityManagerFactoryBuilder() {
        return new EntityManagerFactoryBuilder(new HibernateJpaVendorAdapter(), new HashMap<>(), null);
    }

    @Bean(name = "authEntityManagerFactory")
    public LocalContainerEntityManagerFactoryBean authEntityManagerFactory(
            EntityManagerFactoryBuilder authEntityManagerFactoryBuilder,
            @Qualifier("dataSource") DataSource nbsDataSource ) {
        return authEntityManagerFactoryBuilder
                .dataSource(nbsDataSource)
                .packages("gov.cdc.nbsauthenticator.repositories.models")
                .persistenceUnit("auth")
                .build();
    }

    @Bean(name = "authTransactionManager")
    public PlatformTransactionManager authTransactionManager(
            @Qualifier("authEntityManagerFactory") EntityManagerFactory authEntityManagerFactory ) {
        return new JpaTransactionManager(authEntityManagerFactory);
    }
}
