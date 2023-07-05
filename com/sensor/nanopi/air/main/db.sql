


CREATE SCHEMA `sunpeng` DEFAULT CHARACTER SET utf8 ;



CREATE TABLE `sunpeng`.`sensordata` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `create_time` TIMESTAMP(3) NULL,
  `site` VARCHAR(45) NOT NULL,
  `temperature` VARCHAR(45) NULL,
  `humidity` VARCHAR(45) NULL,
  `co2` VARCHAR(45) NULL,
  `windspeed` VARCHAR(45) NULL,
  PRIMARY KEY (`id`));

#告警信息表
CREATE TABLE `sunpeng`.`log` (
  `id` INT NOT NULL,
  `msg` VARCHAR(45) NULL,
  `site` VARCHAR(45) NULL,
  `starttime` TIMESTAMP NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC));

