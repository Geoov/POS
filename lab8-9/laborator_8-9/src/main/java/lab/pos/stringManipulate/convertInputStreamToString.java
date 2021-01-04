package lab.pos.stringManipulate;

import org.apache.commons.io.IOUtils;

import java.io.IOException;
import java.io.InputStream;
import java.io.StringWriter;
import java.nio.charset.StandardCharsets;

public class convertInputStreamToString {
    public static String convertInputStreamToStringCommonIO(InputStream inputStream)
            throws IOException {

        StringWriter writer = new StringWriter();
        IOUtils.copy(inputStream, writer, StandardCharsets.UTF_8);
        return writer.toString();

    }
}
