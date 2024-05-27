
CREATE TABLE `torrents` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hcode` varchar(45) NOT NULL DEFAULT 'hashcode',
  `path` varchar(1000) NOT NULL DEFAULT '存放路径',
  `filename` varchar(1000) NOT NULL DEFAULT '文件名',
  `creattime` timestamp(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3) COMMENT '''扫描文件时间''',
  PRIMARY KEY (`id`),
  UNIQUE KEY `hashIdx` (`hcode`)
) ENGINE=InnoDB AUTO_INCREMENT=1507 DEFAULT CHARSET=utf8mb4;

CREATE TABLE `torrents_dup` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hcode` varchar(45) NOT NULL DEFAULT 'hashcode',
  `path` varchar(1000) NOT NULL DEFAULT '存放路径',
  `filename` varchar(1000) NOT NULL DEFAULT '文件名',
  `creattime` timestamp(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3) COMMENT '''扫描文件时间''',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=153 DEFAULT CHARSET=utf8mb4;


---查询重复
SELECT *
FROM torrents_dup
WHERE hcode IN (
    SELECT hcode
    FROM torrents_dup
    GROUP BY hcode
    HAVING COUNT(*) > 1
);