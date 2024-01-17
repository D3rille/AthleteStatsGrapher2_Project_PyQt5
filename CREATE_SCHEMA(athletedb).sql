CREATE SCHEMA `athletedb` ;

CREATE TABLE `athletedb`.`positions` (
  `position_name` VARCHAR(45) NOT NULL,
  `position_acronym` VARCHAR(3) NOT NULL,
  PRIMARY KEY (`position_name`));
  
   CREATE TABLE `athletedb`.`teams` (
  `teamName` VARCHAR(45) NOT NULL,
  `wins` INT NOT NULL DEFAULT 0,
  `loses` INT NOT NULL DEFAULT 0,
  `ave_scores` FLOAT NOT NULL DEFAULT 0,
  `ave_assists` FLOAT NOT NULL DEFAULT 0,
  `ave_rebound` FLOAT NOT NULL DEFAULT 0,
  `ave_steals` FLOAT NOT NULL DEFAULT 0,
  `ave_blocks` FLOAT NOT NULL DEFAULT 0,
  `pic_filename` VARCHAR(45) NULL DEFAULT 'photo_placeholder2.png',
  PRIMARY KEY (`teamName`));
  
  CREATE TABLE `athletedb`.`playerinfo` (
  `playerId` VARCHAR(11) NOT NULL,
  `last_name` VARCHAR(45) NOT NULL,
  `first_name` VARCHAR(45) NOT NULL,
  `birthdate` DATE NOT NULL,
  `teamName` VARCHAR(45) NOT NULL,
  `position_name` VARCHAR(45) NOT NULL,
  `jersey_no.` INT NULL,
  `height(ft)` VARCHAR(45) NOT NULL,
  `weight(lbs)` VARCHAR(45) NOT NULL,
  `pic_filename` VARCHAR(45) NOT NULL DEFAULT 'placeholder.jpg',
  PRIMARY KEY (`playerId`));
  
  CREATE TABLE `athletedb`.`playerperformance` (
  `statId` INT NOT NULL AUTO_INCREMENT,
  `playerId` VARCHAR(11) NOT NULL,
  `no_Matches` INT NOT NULL DEFAULT 0,
  `points` INT NOT NULL DEFAULT 0,
  `assists` INT NOT NULL DEFAULT 0,
  `rebounds` INT NOT NULL DEFAULT 0,
  `steals` INT NOT NULL DEFAULT 0,
  `blocks` INT NOT NULL DEFAULT 0,
  PRIMARY KEY (`statId`));
  
ALTER TABLE `athletedb`.`playerinfo` 
ADD INDEX `fk_position_name_idx` (`position_name` ASC) VISIBLE;
;
ALTER TABLE `athletedb`.`playerinfo` 
ADD CONSTRAINT `fk_position_name`
  FOREIGN KEY (`position_name`)
  REFERENCES `athletedb`.`positions` (`position_name`)
  ON DELETE CASCADE
  ON UPDATE NO ACTION;
  
  ALTER TABLE `athletedb`.`playerinfo` 
ADD INDEX `fk_teamName_idx` (`teamName` ASC) VISIBLE;
;
ALTER TABLE `athletedb`.`playerinfo` 
ADD CONSTRAINT `fk_teamName`
  FOREIGN KEY (`teamName`)
  REFERENCES `athletedb`.`teams` (`teamName`)
  ON DELETE CASCADE
  ON UPDATE NO ACTION;
  
  ALTER TABLE `athletedb`.`playerperformance` 
ADD INDEX `fk_playerId_idx` (`playerId` ASC) VISIBLE;
;
ALTER TABLE `athletedb`.`playerperformance` 
ADD CONSTRAINT `fk_playerId`
  FOREIGN KEY (`playerId`)
  REFERENCES `athletedb`.`playerinfo` (`playerId`)
  ON DELETE CASCADE
  ON UPDATE NO ACTION;
  
INSERT INTO `athletedb`.`teams` (`teamName`, `wins`, `loses`, `ave_scores`, `ave_assists`, `ave_rebound`, `ave_steals`, `ave_blocks`, `pic_filename`) VALUES ('Brooklyn Nets', '48', '24', '118.6', '26.8', '44.4', '6.7', '5.3', 'brooklyn_nets.png');
INSERT INTO `athletedb`.`teams` (`teamName`, `wins`, `loses`, `ave_scores`, `ave_assists`, `ave_rebound`, `ave_steals`, `ave_blocks`, `pic_filename`) VALUES ('LA Lakers', '42', '30', '109.5', '24.7', '44.2', '7.8', '5.4', 'la_lakers.png');
INSERT INTO `athletedb`.`teams` (`teamName`, `wins`, `loses`, `ave_scores`, `ave_assists`, `ave_rebound`, `ave_steals`, `ave_blocks`, `pic_filename`) VALUES ('Golden State Warriors', '39', '33', '113.7', '27.7', '43.0', '8.2', '4.8', 'golden_state_warriors.png');

INSERT INTO `athletedb`.`positions` (`position_acronym`, `position_name`) VALUES ('PG', 'Point Guard');
INSERT INTO `athletedb`.`positions` (`position_acronym`, `position_name`) VALUES ('SG', 'Shooting Guard');
INSERT INTO `athletedb`.`positions` (`position_acronym`, `position_name`) VALUES ('SF', 'Small Forward');
INSERT INTO `athletedb`.`positions` (`position_acronym`, `position_name`) VALUES ('PF', 'Power Forward');
INSERT INTO `athletedb`.`positions` (`position_acronym`, `position_name`) VALUES ('C', 'Center');

INSERT INTO `athletedb`.`playerinfo` (`playerId`, `last_name`, `first_name`, `birthdate`, `teamName`, `position_name`, `jersey_no.`, `height(ft)`, `weight(lbs)`, `pic_filename`) VALUES ('1', 'Durant', 'Kevin', '1988-09-29', 'Brooklyn Nets', 'Power Forward', '7', '6.10', '240', 'kevin_durant.png');
INSERT INTO `athletedb`.`playerinfo` (`playerId`, `last_name`, `first_name`, `birthdate`, `teamName`, `position_name`, `jersey_no.`, `height(ft)`, `weight(lbs)`, `pic_filename`) VALUES ('2', 'James', 'Lebron', '1984-12-30', 'LA Lakers', 'Small Forward', '23', '6.9', '250', 'lebron_james.png');
INSERT INTO `athletedb`.`playerinfo` (`playerId`, `last_name`, `first_name`, `birthdate`, `teamName`, `position_name`, `jersey_no.`, `height(ft)`, `weight(lbs)`, `pic_filename`) VALUES ('3', 'Curry', 'Stephen', '1988-03-14', 'Golden State Warriors', 'Point Guard', '30', '6.3', '185', 'stephen_curry.png');

INSERT INTO `athletedb`.`playerperformance` (`statId`, `playerId`, `no_Matches`, `points`, `assists`, `rebounds`, `steals`, `blocks`) VALUES ('1', '1', '1023', '27926', '4238', '7310', '1112', '1149');
INSERT INTO `athletedb`.`playerperformance` (`statId`, `playerId`, `no_Matches`, `points`, `assists`, `rebounds`, `steals`, `blocks`) VALUES ('2', '2', '1570', '42858', '11567', '12099', '2508', '1232');
INSERT INTO `athletedb`.`playerperformance` (`statId`, `playerId`, `no_Matches`, `points`, `assists`, `rebounds`, `steals`, `blocks`) VALUES ('3', '3', '874', '21402', '5688', '4107', '1463', '194');
