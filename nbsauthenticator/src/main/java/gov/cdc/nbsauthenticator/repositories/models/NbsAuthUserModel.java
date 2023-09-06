package gov.cdc.nbsauthenticator.repositories.models;

import  jakarta.persistence.Column;
import  jakarta.persistence.Entity;
import  jakarta.persistence.Id;
import  jakarta.persistence.GeneratedValue;
import	jakarta.persistence.GenerationType;
import  jakarta.persistence.Table;

import	java.sql.Timestamp;

import	lombok.NoArgsConstructor;
import	lombok.Getter;
import	lombok.Setter;

@Entity
@Table(name = "Auth_user", schema="dbo")
@NoArgsConstructor
@Getter
@Setter
public class NbsAuthUserModel {
	private static String TOSTRING_COLUMN_SPACER = ", ";
	
	@Id
	@GeneratedValue( strategy = GenerationType.IDENTITY )
	@Column(name="auth_user_uid")
    private Integer authUserUid;

    @Column(name = "user_id", length = 256, nullable = false)
    private String userId;
    
    @Column(name = "user_type", length = 100, nullable = true)
    private String userType;

    @Column(name = "user_password", length = 100, nullable = true)
    private String userPassword;

    @Override
    public String toString() {
        String sb = this.getAuthUserUid() +
                TOSTRING_COLUMN_SPACER +
                this.getUserId() +
                TOSTRING_COLUMN_SPACER +
                this.getUserType();
    	
        return sb;
    }
}