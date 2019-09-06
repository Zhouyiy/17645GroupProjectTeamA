package edu.cmu.cs.seai.teama.kafkastreamprocess.datamodel;

import lombok.Data;
import lombok.RequiredArgsConstructor;

/**
 * Data model for representing the information of how a user rate a movie.
 */
@Data
@RequiredArgsConstructor
public class RateData {
    private final BasicInfo basicInfo;
    private final int score;
}
