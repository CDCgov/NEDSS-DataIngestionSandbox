package gov.cdc.authtester;

import 	org.json.JSONObject;
import 	org.slf4j.Logger;
import 	org.slf4j.LoggerFactory;
import 	org.springframework.beans.factory.annotation.Value;
import 	org.springframework.boot.CommandLineRunner;
import 	org.springframework.boot.SpringApplication;
import 	org.springframework.boot.autoconfigure.SpringBootApplication;
import 	org.springframework.context.annotation.Configuration;

import 	java.io.BufferedReader;
import 	java.io.InputStreamReader;
import 	java.io.Reader;
import 	java.net.HttpURLConnection;
import 	java.net.URL;
import 	java.net.URLConnection;
import 	java.security.cert.X509Certificate;
import 	java.util.Base64;

import	javax.net.ssl.HttpsURLConnection;
import	javax.net.ssl.TrustManager;
import	javax.net.ssl.X509TrustManager;
import	javax.net.ssl.SSLContext;
import	javax.net.ssl.HostnameVerifier;
import	javax.net.ssl.SSLSession;

@Configuration
@SpringBootApplication
public class AuthServiceDemonostrator implements CommandLineRunner {
	private Logger logger = LoggerFactory.getLogger(AuthServiceDemonostrator.class);

	private static String AUTH_ROLE_CLAIM = "auth_role_nm";
	private static String AUTH_ELR_CLAIM = "ELR Importer";
	private static String AUTH_ECR_CLAIM = "ECR Importer";

	@Value("${auth.url}")
	private String url;

	@Value("${auth.user}")
	private String nbsUser;

	@Value("${auth.password}")
	private String nbsUserPassword;

	public static void main(String[] args) {
		SpringApplication.run(AuthServiceDemonostrator.class, args);
	}

	@Override
	public void run(String... args) throws Exception {
		String[] tokens = demoSignon();
		demoRoles(tokens);
		demoTokenRefresh(tokens);
		System.exit(0);
	}

	private void demoTokenRefresh(String[] tokens) throws Exception {
		String refreshUrl = String.format("%s/nbsauth/token", url);
		logger.info("refreshUrl = {}", refreshUrl);

		String refreshString = getResponse(refreshUrl, tokens[1]);
		String[] refreshTokens = getTokensFromResponse(refreshString);
		if ((null == refreshTokens) || (refreshTokens[0] == null)) {
			logger.error("Token refresh failed, token(s) is/are null, thus returning");
			return;
		}

		logger.info("Token refresh completed. Token = {}, Refresh token = {}", tokens[0], tokens[1]);

	}

	private void demoRoles(String[] tokens) throws Exception {
		String rolesUrl = String.format("%s/nbsauth/roles", url);
		logger.info("rolesUrl = {}", rolesUrl);

		String rolesString = getResponse(rolesUrl, tokens[0]);
		JSONObject jsonObj = new JSONObject(rolesString);
		String authRoleName = (String) jsonObj.get("roles");
		if (null == authRoleName) {
			logger.error("Auth roles not defined, nothing to authorize, thus returning");
			return;
		}

		logger.info("Auth roles = {}", authRoleName);

		boolean isAllowedToLoadElrData = authRoleName.contains(AUTH_ELR_CLAIM) || authRoleName.contains("allow_elr_data_loading");
		boolean isAllowedToLoadEcrData = authRoleName.contains(AUTH_ECR_CLAIM) || authRoleName.contains("allow_ecr_data_loading");

		logger.info("Is allowed to load ELR data = {}", isAllowedToLoadElrData);
		logger.info("Is allowed to load ECR data = {}", isAllowedToLoadEcrData);

		return;
	}

	private String[] demoSignon() throws Exception {
		String encryptedUser = new String(Base64.getEncoder().encode(nbsUser.getBytes()));
		String encryptedPassword = new String(Base64.getEncoder().encode(nbsUserPassword.getBytes()));

		String signonUrl = String.format("%s/nbsauth/signon?user=%s&password=%s",
									url,
									encryptedUser,
									encryptedPassword);

		logger.info("signonUrl = {}", signonUrl);

		String tokensStr = getResponse(signonUrl, "");
		String[] tokens = getTokensFromResponse(tokensStr);
		if ((null == tokens) || (tokens[0] == null)) {
			logger.error("Authentication failed, token(s) is/are null, thus returning");
			return tokens;
		}

		logger.info("Sign-on completed. Token = {}, Refresh token = {}", tokens[0], tokens[1]);
		return tokens;
	}

	private String[] getTokensFromResponse(String tokensResponseStr) throws Exception {
		JSONObject jsonObj = new JSONObject(tokensResponseStr);
		String tokensStr = jsonObj.getString("tokens");
		JSONObject tokensJsonObj = new JSONObject(tokensStr);
		String[] tokens = new String[2];
		tokens[0] = tokensJsonObj.getString("token");
		tokens[1] = tokensJsonObj.getString("refreshToekn");
		return tokens;
	}

	private String getResponse(String requestUrl, String token) throws Exception {
		if( requestUrl.startsWith("https") ) {
			disableTrustStore();
		}

		URL url = new URL(requestUrl);
		URLConnection con = url.openConnection();

		if( requestUrl.startsWith("https") ) {
			HttpsURLConnection https = (HttpsURLConnection) con;
			https.setRequestMethod("POST");

			if(token.length() > 0) {
				https.setRequestProperty("Auth-Token", token);
			}
		}
		else {
			HttpURLConnection http = (HttpURLConnection) con;
			http.setRequestMethod("POST");

			if(token.length() > 0) {
				http.setRequestProperty("Auth-Token", token);
			}
		}

		final Reader reader = new InputStreamReader(con.getInputStream());
		final BufferedReader br = new BufferedReader(reader);

		String line = "";
		String responseString = "";
		while ((line = br.readLine()) != null) {
			responseString += line;
		}

		br.close();
		return responseString;
	}

	private void disableTrustStore() throws Exception {
		TrustManager[] trustAllCerts = new TrustManager[]{
				new X509TrustManager() {
					public java.security.cert.X509Certificate[] getAcceptedIssuers() {
						return null;
					}

					public void checkClientTrusted(X509Certificate[] certs, String authType) {
					}

					public void checkServerTrusted(X509Certificate[] certs, String authType) {
					}
				}
		};

		final SSLContext sc = SSLContext.getInstance("SSL");
		sc.init(null, trustAllCerts, new java.security.SecureRandom());
		HttpsURLConnection.setDefaultSSLSocketFactory(sc.getSocketFactory());

		HostnameVerifier allHostsValid = new HostnameVerifier() {
			public boolean verify(String hostname, SSLSession session) {
				return true;
			}
		};

		HttpsURLConnection.setDefaultHostnameVerifier(allHostsValid);
	}
}
