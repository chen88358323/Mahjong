
CREATE TABLE `sunpeng`.`sensordata` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `create_time` TIMESTAMP(3) NULL,
  `site` VARCHAR(45) NOT NULL,
  `temperature` VARCHAR(45) NULL,
  `humidity` VARCHAR(45) NULL,
  `co2` VARCHAR(45) NULL,
  `windspeed` VARCHAR(45) NULL,
  PRIMARY KEY (`id`));
