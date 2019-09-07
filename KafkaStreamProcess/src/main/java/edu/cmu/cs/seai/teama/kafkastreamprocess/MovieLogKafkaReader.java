package edu.cmu.cs.seai.teama.kafkastreamprocess;

import com.google.gson.Gson;
import edu.cmu.cs.seai.teama.kafkastreamprocess.datamodel.BasicInfo;
import edu.cmu.cs.seai.teama.kafkastreamprocess.datamodel.RateData;
import edu.cmu.cs.seai.teama.kafkastreamprocess.datamodel.WatchData;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.json.JSONObject;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;

import java.nio.charset.Charset;
import java.time.Duration;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Properties;


/**
 * Class for retrieving data from Kafka topic, pre-processing the raw data,
 * and putting processed data into data store.
 * <p>
 * There are two kinds of data from Kafka topic - movielog. First one is
 * "WatchData" which record what movie a user watched. Second one is
 * "RateData" which record information that a user score a movie.
 */
public class MovieLogKafkaReader {
    /**
     * Server IP should be 128.2.204.215. Here an SSH tunnel with ssh -L
     * 9092:localhost:9092 tunnel@128.2.204.215 -NT command to forwards the
     * port 9092 of the original server to local machine.
     */
    private static final String BOOTSTRAP_SERVER = "localhost:9092";
    private static final String GROUP_ID = "MovieLog1";
    private static final String KEY_DESERIALIZER = "org.apache.kafka.common" +
            ".serialization.StringDeserializer";
    private static final String VALUE_DESERIALIZER = "org.apache.kafka.common" +
            ".serialization.StringDeserializer";
    private static final String MOVIE_URL_PREFIX = "http://128.2.204" +
            ".215:8080/movie/";
    private static final String USER_URL_PREFIX = "http://128.2.204" +
            ".215:8080/user/";
    private static final APIAccessor API_ACCESSOR = new APIAccessor();
    private static final Gson GSON = new Gson();
    private static final String FILE_PATH_PREFIX = "/Users/chenxili/Desktop/";

    /**
     * Main method for the whole program.
     * @param args only one arg -> how many data need to collect (sum of the
     *             number of RateData and WatchData).
     * @throws Exception Throw exception when write result to json encouters
     * error.
     */
    public static void main(String[] args) throws Exception {
        Properties props = new Properties();
        props.put("bootstrap.servers", BOOTSTRAP_SERVER);
        props.put("group.id", GROUP_ID);
        props.put("key.deserializer", KEY_DESERIALIZER);
        props.put("value.deserializer", VALUE_DESERIALIZER);

        // Create the consumer to read the data from topic
        KafkaConsumer<String, String> consumer = new KafkaConsumer<String,
                String>(props);

        // Create the topic list that need to be read
        List<String> topics = new ArrayList<>();
        topics.add("movielog");

        // Subscribe a topic
        consumer.subscribe(topics);

        Map<String, Map<String, WatchData>> watchDataMap = new HashMap<>();
        Map<String, Map<String, RateData>> rateDataMap = new HashMap<>();
        Map<String, String> movieDataStore = new HashMap<>();
        Map<String, String> userDataStore = new HashMap<>();
        int counter = 0;

        try {
            while (counter < Integer.parseInt(args[0])) {
                //Define the time-out interval and controls how long poll
                // will block if data is not available in the consumer buffer.
                ConsumerRecords<String, String> records =
                        consumer.poll(Duration.ofMillis(100));
                for (ConsumerRecord<String, String> record : records) {
                    BasicInfo basicInfo = constructBasicInfo(record);
                    updateDataStore(basicInfo, movieDataStore,
                            userDataStore);
                    if (isRateData(record)) {
                        RateData rateData =
                                constructRateData(basicInfo, record);
                        rateDataMap.putIfAbsent(basicInfo.getUserId(),
                                new HashMap<>());
                        rateDataMap.get(basicInfo.getUserId()).put(basicInfo.getAccquireTime(), rateData);
                    } else {
                        WatchData watchData =
                                constructWatchData(basicInfo, record);
                        watchDataMap.putIfAbsent(basicInfo.getUserId(),
                                new HashMap<>());
                        watchDataMap.get(basicInfo.getUserId()).put(basicInfo.getAccquireTime(),
                                watchData);
                    }
                    counter++;
                    if (counter >= Integer.parseInt(args[0])) break;
                    System.out.println(counter);
                }
            }
        } finally {
            consumer.close();
        }

        // write result to json file
        writeToFile("WatchData1000.json", GSON.toJson(watchDataMap));
        writeToFile("RateData1000.json", GSON.toJson(rateDataMap));
        writeToFile("MovieDataStore.json", GSON.toJson(movieDataStore));
        writeToFile("UserDataStore.json", GSON.toJson(userDataStore));
    }

    /**
     * Helper method to update the movie information data store and user
     * information data store. This method prevent the duplicate invoking and
     * storing the same data.
     *
     * @param basicInfo BasicInfo
     * @param movieDataStore data store for storing movie information
     * @param userDataStore  data store for storing user information
     * @return true if successfully update both data store.
     */
    private static void updateDataStore(BasicInfo basicInfo,
                                                  Map<String, String> movieDataStore,
                                                  Map<String, String> userDataStore) {
        String movieInfo =
                API_ACCESSOR.getResult(MOVIE_URL_PREFIX + basicInfo.getMovieId());
        String userInfo =
                API_ACCESSOR.getResult(USER_URL_PREFIX + basicInfo.getUserId());
        if (!movieInfo.equals("") && !userInfo.equals("")) {
            movieDataStore.putIfAbsent(getTMDB_ID(movieInfo),
                    movieInfo);
            userDataStore.putIfAbsent(basicInfo.getUserId(), userInfo);
            basicInfo.setMovieId(getTMDB_ID(movieInfo));
        }
    }

    private static String getTMDB_ID(String movieInfo) {
        JSONObject jsonObject = new JSONObject(movieInfo);
        return jsonObject.getInt("tmdb_id") + "";
    }

    /**
     * Helper method for constructing BasicInfo by ConsumerRecord
     *
     * @param record ConsumerRecord
     * @return BasicInfo
     */
    private static BasicInfo constructBasicInfo(ConsumerRecord<String,
            String> record) {
        String[] messages = record.value().split(",");
        String[] movieInfo = messages[2].split("/");
        String movieId = "";
        if (movieInfo.length == 5) {
            movieId = movieInfo[3];
        } else {
            movieId = movieInfo[2].split("=")[0];
        }
        BasicInfo basicInfo = new BasicInfo(record.offset(), messages[0].trim(),
                messages[1].trim());
        basicInfo.setMovieId(movieId);
        return basicInfo;
    }

    /**
     * Helper method to check if current raw data is a RateData or WatchData
     *
     * @param record ConsumerRecord
     * @return true if this is a RateData
     */
    private static boolean isRateData(ConsumerRecord<String,
            String> record) {
        return record.value().split(",")[2].split("/").length != 5;
    }

    /**
     * Helper method to construct WatchData by BasicInfo and ConsumerRecord.
     *
     * @param basicInfo BasicInfo
     * @param record    ConsumerRecord
     * @return WatchData object
     */
    private static WatchData constructWatchData(BasicInfo basicInfo,
                                                ConsumerRecord<String,
            String> record) {
        String[] watchInfo =
                record.value().split(",")[2].split("/")[4].split("\\.");
        return new WatchData(basicInfo, Integer.parseInt(watchInfo[0]),
                watchInfo[1]);
    }

    /**
     * Helper method to construct RateData by BasicInfo and ConsumerRecord.
     *
     * @param basicInfo BasicInfo
     * @param record    ConsumerRecord
     * @return RateData object
     */
    private static RateData constructRateData(BasicInfo basicInfo,
                                              ConsumerRecord<String, String> record) {
        return new RateData(basicInfo,
                Integer.parseInt(record.value().split(",")[2].split("/")[2].split(
                        "=")[1]));
    }

    /**
     * Helper method to write json string into json file
     *
     * @param fileName name of the file
     * @param content  json string
     * @throws IOException
     */
    private static void writeToFile(String fileName, String content) throws IOException {
        try (BufferedWriter writer =
                     new BufferedWriter(new FileWriter(FILE_PATH_PREFIX + fileName, Charset.forName("UTF-8")))) {
            writer.write(content);
        }
    }
}
