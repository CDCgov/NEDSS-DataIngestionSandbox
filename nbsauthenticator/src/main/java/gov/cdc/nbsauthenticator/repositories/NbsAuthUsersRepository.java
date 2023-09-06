package gov.cdc.nbsauthenticator.repositories;

import  gov.cdc.nbsauthenticator.repositories.models.NbsAuthUserModel;

import	org.springframework.stereotype.Repository;
import  org.springframework.data.jpa.repository.JpaRepository;
import 	org.springframework.data.jpa.repository.Query;
import  org.springframework.data.repository.query.Param;

import	java.math.BigInteger;

@Repository
public interface NbsAuthUsersRepository extends JpaRepository<NbsAuthUserModel, Integer> {
	@Query(value = "select max(auth_user_uid) from Auth_user", nativeQuery = true)
    BigInteger getMaxAuthUserId();

    @Query(value = "select auth_user_uid from Auth_user where user_id = :userId and user_password = :userPassword", nativeQuery = true)
    BigInteger getAuthUserIdUsingUserIdAndPassword(@Param("userId") String user, @Param("userPassword") String userPassword);
}
