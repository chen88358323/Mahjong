
CREATE DATABASE `torr` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;


    CREATE TABLE `filedetails_dup` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `hcode` varchar(50) NOT NULL DEFAULT 'hash	code',
      `isdir` int(1) NOT NULL,
      `path` varchar(500) NOT NULL DEFAULT '存放路径',
      `filename` varchar(500) NOT NULL DEFAULT '文件名',
      `creattime` timestamp(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3) COMMENT '''扫描文件时间''',
      `modifiedtime` timestamp(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3) COMMENT '''文件修改时间''',
      `filetype` varchar(10) DEFAULT NULL,
      `belong` varchar(45) DEFAULT NULL COMMENT '分类',
      `keyword` varchar(200) DEFAULT NULL,
      `systemdriver` varchar(50) DEFAULT NULL COMMENT '系统盘符',
      `platformscan` varchar(10) DEFAULT NULL COMMENT '该文件扫描的系统',
      `filesize` float NOT NULL DEFAULT '0' COMMENT '文件大小单位 Mb',
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB AUTO_INCREMENT=792 DEFAULT CHARSET=utf8mb4;



CREATE TABLE `filedetails` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hcode` varchar(50) NOT NULL DEFAULT 'hashcode',
  `isdir` int(1) NOT NULL,
  `path` varchar(500) NOT NULL DEFAULT '存放路径',
  `filename` varchar(500) NOT NULL DEFAULT '文件名',
  `creattime` timestamp(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3) COMMENT '''扫描文件时间''',
  `modifiedtime` timestamp(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3) COMMENT '''文件修改时间''',
  `filetype` varchar(10) DEFAULT NULL,
  `belong` varchar(45) DEFAULT NULL COMMENT '分类',
  `keyword` varchar(200) DEFAULT NULL,
  `systemdriver` varchar(50) DEFAULT NULL COMMENT '系统盘符',
  `platformscan` varchar(10) DEFAULT NULL COMMENT '该文件扫描的系统',
  `filesize` float NOT NULL DEFAULT '0' COMMENT '文件大小单位 Mb',
  PRIMARY KEY (`id`),
  UNIQUE KEY `hcode_idx` (`hcode`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4;