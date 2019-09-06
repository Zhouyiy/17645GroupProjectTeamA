# Criterias

## Data gathering and cleaning

Describe the data you used for learning (provided and external), how you gathered it, and describe how you cleaned the data.

1. Kafka stream
    1. GET /data
        - Timestamp
        - user_id
        - movie_name
        - chunk_number
            - /data/m/{movie name separated by +}+{year}/{chunk_number}.mpg
                - We can get how long the user has watched a certain movie from chunk_number
    2. GET /rate
        - Timestamp
        - user_id
        - movie_name
        - rate
            - /rate/{movie name}={rate}
2. http://128.2.204.215:8080/user/<userid>
    - user_id
    - age
    - occupation
    - gender
3.  http://128.2.204.215:8080/movie/<movieid> 
    - id
    - tmdb_id: num
    - imdb_id: str
    - title
    - ~~original_title~~
    - adult
    - belongs_to_collection: {}
    - budget
    - genres:[{id, name}]
    - ~~homepage~~
    - original_language
    - ~~overview~~
    - popularity: a number in str
    - ~~poster_path: (path to a jpg file)~~
    - production_companies: []
    - production_countries: [{iso_3166_1, name}]
    - release_date
    - revenue
    - runtime
    - ~~spoken_languages: [{iso_639_1, name}]~~
    - ~~status~~
    - tagline
    - vote_average
    - vote_count

### Why users and movies are API requests rather than API?

## Features

Provide a full list of all features used in the model and a short description of how they were extracted. Provide a pointer to the implementation of the feature extraction process, as appropriate.

## Learning

Describe the learning techniques used and provide a pointer to the implementation. Provide a brief justification why you decided to use this specific technique and implementation. Provide a pointer to the final model learned.

### Thoughts

It can be a user-to-movie, or movie-to-movie.

content-based filtering / collaborative filtering -> embedding -> similarities(cosine, dot product, euclidean)

- Content-based filtering: simple idea
    - https://developers.google.com/machine-learning/recommendation/content-based/basics

https://developers.google.com/machine-learning/recommendation/labs/movie-rec-programming-exercise

## Evaluation

Describe how you evaluated the model. This should include at least a description of the evaluation metric and the evaluation data. Briefly justify both the used metric and how you separated evaluation data.

## Evaluation results

Provide the evaluation results for the final model. In addition, demonstrate how the evaluation helped in designing the model by including results for one significant decision during the modeling process (e.g., comparing two learning techniques or comparing results with and without a certain feature). Provide a pointer to the corresponding artifacts.

## Process reflection 

Think back about your team's process and reflect about what worked well and what did not. Focus especially on problems regarding teamwork and process and discuss what you would do different if you would do the assignment again.
