package gov.cdc.nbsauthenticator.repositories;

import  gov.cdc.nbsauthenticator.repositories.models.NbsAuthUserRoleModel;

import	org.springframework.stereotype.Repository;
import  org.springframework.data.jpa.repository.JpaRepository;
import 	org.springframework.data.jpa.repository.Query;
import  org.springframework.data.repository.query.Param;

import  java.util.List;

@Repository
public interface NbsAuthUserRolesRepository extends JpaRepository<NbsAuthUserRoleModel, String> {
    @Query(value = "select auth_user_role_uid, prog_area_cd, auth_role_nm, jurisdiction_cd from Auth_user_role where auth_user_uid = :authUserId", nativeQuery = true)
    List<NbsAuthUserRoleModel> getAuthRolesForAuthUserId(@Param("authUserId") int authUserId);
}
