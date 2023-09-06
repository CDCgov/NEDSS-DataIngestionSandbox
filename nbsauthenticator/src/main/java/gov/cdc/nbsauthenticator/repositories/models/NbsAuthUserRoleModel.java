package gov.cdc.nbsauthenticator.repositories.models;

import  jakarta.persistence.Column;
import  jakarta.persistence.Entity;
import  jakarta.persistence.Id;
import  jakarta.persistence.Table;

import	lombok.NoArgsConstructor;
import	lombok.Getter;
import	lombok.Setter;

@Entity
@Table(name = "Auth_user_role", schema="dbo")
@NoArgsConstructor
@Getter
@Setter
public class NbsAuthUserRoleModel {
	private static String TOSTRING_COLUMN_SPACER = ", ";

    @Id
    @Column(name="auth_user_role_uid")
    private Integer authUserRoleUid;

    @Column(name = "prog_area_cd", length = 100, nullable = true)
    private String progAreaCd;

    @Column(name = "auth_role_nm", length = 100, nullable = false)
    private String authRoleNm;


    @Column(name = "jurisdiction_cd", length = 100, nullable = true)
    private String jurisdictionCd;
}