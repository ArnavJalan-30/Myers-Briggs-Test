create database final_proj;
use final_proj;

CREATE TABLE `personality_questions` (
  `questionid` int NOT NULL,
  `questiondesc` varchar(1000) NOT NULL,
  `personal_type` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`questionid`)
);
CREATE TABLE `questionoptions` (
  `questionoptionid` int NOT NULL,
  `optiondescription` varchar(100) NOT NULL,
  `optionmarks` int DEFAULT NULL,
  `questionid` int NOT NULL,
  PRIMARY KEY (`questionoptionid`),
  KEY `questionid_fk_idx` (`questionid`),
  CONSTRAINT `questionid_fk` FOREIGN KEY (`questionid`) REFERENCES `personality_questions` (`questionid`)
);
CREATE TABLE `personqa` (
  `personqaid` int NOT NULL AUTO_INCREMENT,
  `person_name` varchar(100) DEFAULT NULL,
  `questionoptionid` int DEFAULT NULL,
  `questionid` int DEFAULT NULL,
  `age` int DEFAULT NULL,
  `phone_no` bigint NOT NULL,
  PRIMARY KEY (`personqaid`),
  KEY `questionoptionid_fk_idx` (`questionoptionid`),
  KEY `questionid_fk_idx` (`questionid`),
  CONSTRAINT `question_fk` FOREIGN KEY (`questionid`) REFERENCES `personality_questions` (`questionid`),
  CONSTRAINT `questionoptionid_fk` FOREIGN KEY (`questionoptionid`) REFERENCES `questionoptions` (`questionoptionid`)
);



CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vw_getperson` AS select distinct concat(`personqa`.`person_name`,' | ',`personqa`.`phone_no`) AS `person` from `personqa`;
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vw_getquestionoption` AS select concat(`a`.`questiondesc`,'(',`a`.`questionid`,')') AS `questiondesc`,max((case when (`b`.`optiondescription` = 'Strongly Agree') then concat(`b`.`optiondescription`,'(',`b`.`questionoptionid`,')') else NULL end)) AS `Option1`,max((case when (`b`.`optiondescription` = 'Agree') then concat(`b`.`optiondescription`,'(',`b`.`questionoptionid`,')') else NULL end)) AS `Option2`,max((case when (`b`.`optiondescription` = 'Disagree') then concat(`b`.`optiondescription`,'(',`b`.`questionoptionid`,')') else NULL end)) AS `Option3`,max((case when (`b`.`optiondescription` = 'Strongly Disagree') then concat(`b`.`optiondescription`,'(',`b`.`questionoptionid`,')') else NULL end)) AS `Option4` from (`personality_questions` `a` left join `questionoptions` `b` on((`a`.`questionid` = `b`.`questionid`))) group by `a`.`questionid`;



INSERT INTO personality_questions VALUES (1,'I avoid being alone','E-I'),(2,'Being around lots of people energizes me','E-I'),(3,'I enjoy being the center of attention','S-N'),(4,'I dislike being in competition with others','S-N'),(5,'I would rather go with the flow than have a set schedule','T-F'),(6,'I avoid arguing, even when I disagree','T-F'),(7,'I spend time seeking out new experiences','J-P'),(8,'I like thinking about the mysteries of the universe','J-P');
INSERT INTO questionoptions VALUES (1,'Strongly Agree',2,1),(2,'Agree',1,1),(3,'Disagree',-1,1),(4,'Strongly Disagree',-2,1),(5,'Strongly Agree',2,2),(6,'Agree',1,2),(7,'Disagree',-1,2),(8,'Strongly Disagree',-2,2),(9,'Strongly Agree',2,3),(10,'Agree',1,3),(11,'Disagree',-1,3),(12,'Strongly Disagree',-2,3),(13,'Strongly Agree',2,4),(14,'Agree',1,4),(15,'Disagree',-1,4),(16,'Strongly Disagree',-2,4),(17,'Strongly Agree',2,5),(18,'Agree',1,5),(19,'Disagree',-1,5),(20,'Strongly Disagree',-2,5),(21,'Strongly Agree',2,6),(22,'Agree',1,6),(23,'Disagree',-1,6),(24,'Strongly Disagree',-2,6),(25,'Strongly Agree',2,7),(26,'Agree',1,7),(27,'Disagree',-1,7),(28,'Strongly Disagree',-2,7),(29,'Strongly Agree',2,8),(30,'Agree',1,8),(31,'Disagree',-1,8),(32,'Strongly Disagree',-2,8);
