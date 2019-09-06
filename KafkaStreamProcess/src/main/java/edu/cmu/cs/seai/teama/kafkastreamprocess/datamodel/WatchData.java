package edu.cmu.cs.seai.teama.kafkastreamprocess.datamodel;

import lombok.Data;
import lombok.RequiredArgsConstructor;

/**
 * Data model used to represent the information of a user watch a movie.
 */
@Data
@RequiredArgsConstructor
public class WatchData {
    private final BasicInfo basicInfo;
    private final int blockId;
    private final String mediaType;
}
