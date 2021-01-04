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
import java.nio.file.FileAlreadyExistsException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

import static org.junit.Assert.*;

import static lab.pos.stringManipulate.convertInputStreamToString.convertInputStreamToStringCommonIO;
import static lab.pos.stringManipulate.randomStringGenerator.generateString;


@Endpoint
public class LoginEndpoint {
    private static final String NAMESPACE_URI = "http://localhost:5000/api/library/users";

//    @PayloadRoot(namespace = NAMESPACE_URI, localPart = "getUserRequest")
//    @ResponsePayload
//    public GetUserResponse getUser(@RequestPayload GetUserRequest request) throws IOException {
//        GetUserResponse response = new GetUserResponse();
//        ServiceStatus serviceStatus = new ServiceStatus();
//
//        String urlString = "http://localhost:5000/api/library/users?email=" + '\'' + request.getUsername() + '\'';
//        URL url = new URL(urlString);
//        URLConnection conn = url.openConnection();
//        InputStream inputStream = conn.getInputStream();
//
//        String fullResponseBody = convertInputStreamToStringCommonIO(inputStream);
//        String responseBody = fullResponseBody.substring(15, fullResponseBody.length() - 3);
//
//        Gson g = new Gson();
//        User user = g.fromJson(responseBody, User.class);
//
//        if(!responseBody.equals(""))
//        {
//            if(user.getPassword().equals(request.getPassword())) {
//                serviceStatus.setStatusCode("200");
//                serviceStatus.setMessage("SUCCESS");
//
//                String uRole = user.getRole();
//
//            }else {
//                serviceStatus.setStatusCode("403");
//                serviceStatus.setMessage("WRONG CREDENTIALS");
//            }
//        } else{
//            serviceStatus.setStatusCode("404");
//            serviceStatus.setMessage("NOT FOUND");
//        }
//
//        response.setUser(user);
//        response.setServiceStatus(serviceStatus);
//
//        return response;
//    }

    @PayloadRoot(namespace = NAMESPACE_URI, localPart = "getUserRequest")
    @ResponsePayload
    public GetLimitedUserResponse getLimitedUser(@RequestPayload GetUserRequest request) throws IOException {
        GetLimitedUserResponse response = new GetLimitedUserResponse();
        ServiceStatus serviceStatus = new ServiceStatus();

        String urlString = "http://localhost:5000/api/library/users?email=" + '\'' + request.getUsername() + '\'';
        URL url = new URL(urlString);
        URLConnection conn = url.openConnection();
        InputStream inputStream = conn.getInputStream();

        String fullResponseBody = convertInputStreamToStringCommonIO(inputStream);
        String responseBody = fullResponseBody.substring(15, fullResponseBody.length() - 3);

        Gson g = new Gson();
        User user = g.fromJson(responseBody, User.class);

        if(!responseBody.equals(""))
        {
            if(user.getPassword().equals(request.getPassword())) {
                serviceStatus.setStatusCode("200");
                serviceStatus.setMessage("SUCCESS");

                response.setEmail(user.getEmail());
                response.setRole(user.getRole());
                response.setServiceStatus(serviceStatus);

                String uuidTxt = generateString();
                response.setFolderId(uuidTxt);

                String userInfo = user.getEmail() + "\n" + user.getRole();

                Path path = Paths.get("/home/geov/Public/facultate/Anul_IV/POS/lab5/SoapServices_5/user-details/" + uuidTxt + ".txt");

                try {
                    Files.createFile(path);
                } catch(FileAlreadyExistsException e){
                    serviceStatus.setStatusCode("500");
                    serviceStatus.setMessage("File already exist");
                    response.setServiceStatus(serviceStatus);
                }

                BufferedWriter writer = new BufferedWriter(new FileWriter("/home/geov/Public/facultate/Anul_IV/POS/lab5/SoapServices_5/user-details/" + uuidTxt + ".txt"));
                writer.write(userInfo);

                writer.close();

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
    public GetUserRoleResponse getUserRole(@RequestPayload GetUserRoleRequest request) throws IOException {
        GetUserRoleResponse response = new GetUserRoleResponse();
        ServiceStatus serviceStatus = new ServiceStatus();

        BufferedReader brTest = new BufferedReader(new FileReader("/home/geov/Public/facultate/Anul_IV/POS/lab5/SoapServices_5/user-details/" + request.getNumeFisier() + ".txt"));
        String fileUsername = brTest.readLine();

        if(fileUsername.equals(request.getUsername()))
        {
            String fileRole = Files.readAllLines(Paths.get("/home/geov/Public/facultate/Anul_IV/POS/lab5/SoapServices_5/user-details/" + request.getNumeFisier() + ".txt")).get(1);
            response.setRole(fileRole);
            serviceStatus.setStatusCode("200");
            serviceStatus.setMessage("SUCCESS");
            response.setServiceStatus(serviceStatus);
        }
        return response;
    }

    @PayloadRoot(namespace = NAMESPACE_URI, localPart = "deleteUserFileRequest")
    @ResponsePayload
    public DeleteUserFileResponse getUserRole(@RequestPayload DeleteUserFileRequest request) throws IOException {
        DeleteUserFileResponse response = new DeleteUserFileResponse();
        ServiceStatus serviceStatus = new ServiceStatus();

        File fileToDelete = new File("/home/geov/Public/facultate/Anul_IV/POS/lab5/SoapServices_5/user-details/" + request.getNumeFisier() + ".txt");
        boolean success = fileToDelete.delete();

        if(success)
        {
            serviceStatus.setStatusCode("204");
            serviceStatus.setMessage("NO CONTENT");
            response.setServiceStatus(serviceStatus);
        }

        return response;
    }
}
