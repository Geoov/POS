package lab.pos.soap;

import com.google.gson.Gson;
import localhost._5000.api.library.users.*;

import org.springframework.ws.server.endpoint.annotation.Endpoint;
import org.springframework.ws.server.endpoint.annotation.PayloadRoot;
import org.springframework.ws.server.endpoint.annotation.RequestPayload;
import org.springframework.ws.server.endpoint.annotation.ResponsePayload;

import java.io.*;

import java.net.URL;
import java.net.URLConnection;

import java.nio.file.*;
import java.util.Base64;
import java.util.Calendar;
import java.util.Date;

import static lab.pos.stringManipulate.convertInputStreamToString.convertInputStreamToStringCommonIO;

//import io.jsonwebtoken.Claims;
//import io.jsonwebtoken.Jws;
//import io.jsonwebtoken.Jwts;
//import io.jsonwebtoken.SignatureAlgorithm;

import com.auth0.jwt.JWT;
import static com.auth0.jwt.algorithms.Algorithm.HMAC512;

@Endpoint
public class LoginEndpoint {
    private static final String NAMESPACE_URI = "http://localhost:5000/api/library/users";
    private final String SECRET_KEY = Base64.getEncoder().encodeToString("\"Te saluta fratele!\"".getBytes());

    @PayloadRoot(namespace = NAMESPACE_URI, localPart = "getUserRequest")
    @ResponsePayload
    public GetUserResponse getUser(@RequestPayload GetUserRequest request) throws IOException {
        GetUserResponse response = new GetUserResponse();
        ServiceStatus serviceStatus = new ServiceStatus();

        String urlString = "http://localhost:5005/api/library/users?email=" + request.getUsername() + "";
        URL url = new URL(urlString);

        URLConnection hc = url.openConnection();
        hc.setRequestProperty("User-Agent", "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.4; en-US; rv:1.9.2.2) " +
                "Gecko/20100316 Firefox/3.6.2");

        URLConnection conn = url.openConnection();
        InputStream inputStream = conn.getInputStream();

        String fullResponseBody = convertInputStreamToStringCommonIO(inputStream);
        String responseBody = fullResponseBody.substring(18, fullResponseBody.length() - 4);

        Gson g = new Gson();
        User user = g.fromJson(responseBody, User.class);

        if(!responseBody.equals(""))
        {
            if(user.getPassword().equals(request.getPassword())) {
                serviceStatus.setStatusCode("200");
                serviceStatus.setMessage("SUCCESS");
                response.setServiceStatus(serviceStatus);

                Calendar cal = Calendar.getInstance();
                cal.setTime(new Date());
                cal.add(Calendar.HOUR_OF_DAY, 1);

//                String jwtToken = Jwts.builder().setSubject(user.getRole())
//                                    .setExpiration(cal.getTime())
//                                    .setIssuer("https://www.iana.org/assignments/jwt/jwt.xhtml")
//                                    .signWith(SignatureAlgorithm.HS512, SECRET_KEY)
//                        .setId()
//                                    .compact();

                String uniqueIdPerUser = Base64.getEncoder().encodeToString(user.getEmail().getBytes());

                Path path = Paths.get("/home/geov/Public/facultate/Anul_IV/POS/lab5/laborator_5/users_jti/"
                        + uniqueIdPerUser + ".txt");
                try {
                    Files.createFile(path);
                } catch(FileAlreadyExistsException e){
//                    serviceStatus.setStatusCode("500");
//                    serviceStatus.setMessage("File already exist");
//                    response.setServiceStatus(serviceStatus);
                }

                String subject = user.getRole() + ":" + user.getId();

                String jwtToken = JWT.create()
                        .withSubject(subject)
                        .withExpiresAt(cal.getTime())
                        .withIssuer(user.getEmail())
                        .withJWTId(uniqueIdPerUser)
                        .sign(HMAC512(SECRET_KEY.getBytes()));

                BufferedWriter writer = new BufferedWriter(new FileWriter("/home/geov/Public/facultate/" +
                        "Anul_IV/POS/lab5/laborator_5/users_jti/" + uniqueIdPerUser + ".txt"));
                writer.write(jwtToken);
                writer.close();

                response.setCookie(uniqueIdPerUser);
                response.setToken(jwtToken);
            }else {
                serviceStatus.setStatusCode("403");
                serviceStatus.setMessage("WRONG CREDENTIALS");
                response.setServiceStatus(serviceStatus);
            }
        } else{
            serviceStatus.setStatusCode("404");
            serviceStatus.setMessage("NOT FOUND");
            response.setServiceStatus(serviceStatus);
        }
        return response;
    }

    @PayloadRoot(namespace = NAMESPACE_URI, localPart = "getUserRoleRequest")
    @ResponsePayload
    public GetUserRoleResponse deleteUserFile(@RequestPayload GetUserRoleRequest request) throws IOException {
        GetUserRoleResponse response = new GetUserRoleResponse();
        ServiceStatus serviceStatus = new ServiceStatus();
        String cookie = "";
        String token = "";

        String[] cookie_array = request.getCookie().split(";");
        cookie = cookie_array[0];

        String[] token_array = request.getToken().split("Bearer ");
        try {
            token = token_array[1];
        } catch (ArrayIndexOutOfBoundsException e){
            token = token_array[0];
        }

        try {
            BufferedReader brTest = new BufferedReader(new FileReader("/home/geov/Public/facultate/Anul_IV/" +
                    "POS/lab5/laborator_5/users_jti/" + cookie + ".txt"));
            brTest.readLine();
        } catch(FileNotFoundException e) {
            serviceStatus.setStatusCode("404");
            serviceStatus.setMessage("File not found");
            response.setServiceStatus(serviceStatus);

            return response;
        }

        String subject =  JWT.require(HMAC512(SECRET_KEY.getBytes()))
                .build()
                .verify(token)
                .getSubject();


        String[] subjectSplitted = subject.split(":");
        response.setRole(subjectSplitted[0]);
        response.setId(subjectSplitted[1]);

        serviceStatus.setStatusCode("200");
        serviceStatus.setMessage("SUCCESS");
        response.setServiceStatus(serviceStatus);

        return response;
    }

    @PayloadRoot(namespace = NAMESPACE_URI, localPart = "deleteUserFileRequest")
    @ResponsePayload
    public DeleteUserFileResponse deleteIdentity(@RequestPayload DeleteUserFileRequest request) {
        DeleteUserFileResponse response = new DeleteUserFileResponse();
        ServiceStatus serviceStatus = new ServiceStatus();
        String cookie = "";

        String[] cookie_array = request.getCookie().split(";");
        cookie = cookie_array[0];

        File fileToDelete = new File("/home/geov/Public/facultate/Anul_IV/POS/lab5/laborator_5/users_jti/"
                + cookie + ".txt");

        boolean success = fileToDelete.delete();

        if(success)
        {
            serviceStatus.setStatusCode("204");
            serviceStatus.setMessage("NO CONTENT");
        } else {
            serviceStatus.setStatusCode("404");
            serviceStatus.setMessage("FILE NOT FOUND");
        }

        response.setServiceStatus(serviceStatus);
        return response;

    }
}
