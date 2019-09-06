package edu.cmu.cs.seai.teama.kafkastreamprocess;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.URL;
import java.nio.charset.Charset;

/**
 * Class used to query API through HTTP method and get the json content.
 */
public class APIAccessor {
    /**
     * Method to get json content by querying API through HTTP method.
     * @param url URL
     * @return json content
     */
    public String getResult(String url) {
        StringBuilder stringBuilder = new StringBuilder();
        try {
            InputStream inputStream = new URL(url).openStream();
            BufferedReader bufferedReader =
                    new BufferedReader(new InputStreamReader(inputStream, Charset.forName("UTF-8")));
            int c;
            while ((c = bufferedReader.read()) != -1) {
                stringBuilder.append((char) c);
            }
            inputStream.close();
            bufferedReader.close();
            return stringBuilder.toString();
        } catch (IOException e) {
            return stringBuilder.toString();
        }
    }
}
