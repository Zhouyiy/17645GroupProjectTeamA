package edu.cmu.cs.seai.teama.kafkastreamprocess.datamodel;

import lombok.Data;
import lombok.RequiredArgsConstructor;

/**
 * Basic information directly retrieved from Kafka Stream.
 */
@Data
@RequiredArgsConstructor
public class BasicInfo {
    private final long messageId;
    private final String accquireTime;
    private final String userId;
    private String movieId;
}
