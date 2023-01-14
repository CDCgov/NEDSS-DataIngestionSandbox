//package com.ndduc.kafkaconnectordemo;
//
//import com.ndduc.kafkaconnectordemo.Controller.DataController;
//import com.ndduc.kafkaconnectordemo.Model.DataModel;
//import com.ndduc.kafkaconnectordemo.Repository.DataRepository;
//import org.springframework.boot.CommandLineRunner;
//import org.springframework.boot.SpringApplication;
//import org.springframework.boot.autoconfigure.SpringBootApplication;
//import org.springframework.context.annotation.Bean;
//
//import java.util.concurrent.TimeUnit;
//
//@SpringBootApplication
//public class ConsoleApp {
//
//
//    public static void main(String[] args) {
//        SpringApplication.run(ConsoleApp.class, args);
//    }
//
//    @Bean
//    public CommandLineRunner demo(DataRepository repository) {
//        return (args) -> {
//            int id = 10;
//            while(true) {
//                repository.save(new DataModel(String.valueOf(id), "test"));
//                id++;
//                TimeUnit.SECONDS.sleep(3);
//            }
//        };
//    }
//}
