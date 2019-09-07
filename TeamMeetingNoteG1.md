# TeamA Meeting Note G1

## 1. Agenda

#### 1.1 Meet Teams and Say Hello

#### 1.2 Discuss how to collaborate with team members
  
#### 1.3 Read the project requirement document and discuss

#### 1.4 Assign works before next meeting
  
## 2. Deliverables

#### 2.1 Team Collabration 

Offline Meeting: One time a week, Friday Afternoon

Online Meeting: Slack channel https://app.slack.com/client/TN3FD2N6S/CN35APC07

Requirement: Two hours response in the daytime

Documentation Collabration Tool: Google Doc

Project management and collabration Tool: Github

#### 2.2 Project Summerization

Functional Requirement:

1. Generate a movie list that is interesting for a user

Quality Requirement:

1. Todo
  
Design:
  Potential design choices:
  	
  1. How to store data?
	
  2. What model to choose?
	
  3. How to choose test dataset?
	
  4. What if people's interest change ?
	
  5. What language to choose ?

  6. How to use data (i.e. what range of the past data should be used)?
  
#### 2.3 Assignment for Next Meeting
  ChenXi: Kafka stream data engineering design 
  
  Zhouyi: Data Analysis Design
  
  Yuchen: Data Analysis Design
  
# TeamA Meeting Note G1 - Second Meeting

## 1. Agenda

#### 1.1 Review and select recommendation approach

#### 1.2 Review and select evaluation metric
  
#### 1.3 Write Specification and Assign Tasks

## 2. Deliverables

#### 2.1 Recommendation approach

Options: Content-Based, Memery-Based CF(similarity), Model-Based CF(SVD, Matrix Factorization ...)

Choice: Choose Content-Based as base line (Easy to implement, don't need data for user rating), add Model-Based CF (Useful when user rating ratio is small) later

#### 2.2 Evaluation Metric

Option: RMSE, NDCG/MAP, Precision/Recall

Choice: Choose Precision/Recall (User rating number is small also rank metric is hard to get)

#### 2.3 Project Requirement and Tasks

The Data Flow:

	KafkaStream -> Local Data Management Service -> Feature Engineering pipeline -> Model Training and calculating pipeline -> Evaluation 
	

*Local Data Management Service:
	
	Requirement:    1. Design a service that retrieves data from kafka stream and persist locally/external_service
			2. Design an efficient data store method that is easy for querying and updating
			3. Maintain data query command/api which is specified by later consumer (i.e. Feature Engineering)
			4. Extensible (considering updating data ...) (Todo Later)
			
*Feature Engineering pipeline:
	
	Requirement:    1. Design a pipeline which transforms data into feature vector (Movie feature, People feature ...)
			2. Supports flexible feature manipulation (data preprocessing, feature scaling, dimension reduction ... )
			3. Make it easy to add, remove, update feature.
			4. Design a feature vector monitor mechenism (todo later)

*Model Training and Evaluation pipeline
	
	Requirement:    1. Design a pipeline which trainforms feature vector into prediction
			2. Make decision about the model choice
			3. Make decision about the evluation metric choice
			4. Design model quality monitor mechemism (todo later)

Chenxi: Local Data Management Service

Yuchen: Feature Engineering pipeline

Zhouyi: Model Training and Evaluation pipeline


