
CREATE DATABASE `torr` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;


    CREATE TABLE `filedetails_dup` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `hcode` varchar(50) NOT NULL DEFAULT 'hash	code',
      `isdir` int(1) NOT NULL,
      `path` varchar(500) NOT NULL DEFAULT '存放路径',
      `filename` varchar(500) NOT NULL DEFAULT '文件名',
      `creattime` timestamp(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3) COMMENT '''扫描文件时间''',
      `modifiedtime` timestamp(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3) COMMENT '''文件修改时间''',
      `filetype` varchar(50) DEFAULT NULL,
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
  `filetype` varchar(50) DEFAULT NULL,
  `belong` varchar(45) DEFAULT NULL COMMENT '分类',
  `keyword` varchar(200) DEFAULT NULL,
  `systemdriver` varchar(50) DEFAULT NULL COMMENT '系统盘符',
  `platformscan` varchar(10) DEFAULT NULL COMMENT '该文件扫描的系统',
  `filesize` float NOT NULL DEFAULT '0' COMMENT '文件大小单位 Mb',
  PRIMARY KEY (`id`),
  UNIQUE KEY `hcode_idx` (`hcode`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4;


--linux
--SELECT concat(a.systemdriver,a.path,a.filename) as src,
--concat(b.systemdriver,b.path,b.filename) as dup,
--a.filesize,b.filesize
--FROM torr.filedetails  a,torr.filedetails_dup b where a.hcode=b.hcode limit 100;
--
--win
--SELECT concat(a.systemdriver,a.path,'\\',a.filename) as src,
--concat(b.systemdriver,b.path,'\\',b.filename) as dup,
--a.filesize,b.filesize
--FROM torr.filedetails  a,torr.filedetails_dup b where a.hcode=b.hcode limit 100;



SELECT id, hcode, isdir, `path`, filename, creattime, modifiedtime, filetype, belong, keyword, systemdriver, platformscan, filesize
FROM torr.filedetails;


SELECT count(*)
FROM torr.filedetails  a,torr.filedetails_dup b
where a.hcode=b.hcode  and ( a.`path` !=b.`path`
or a.filename !=b.filename )

SELECT concat(a.systemdriver,a.path,'/',a.filename) as src,
concat(b.systemdriver,b.path,'/',b.filename) as dup,
a.filesize,b.filesize,a.hcode,a.id ,b.id
FROM torr.filedetails  a,torr.filedetails_dup b
where a.hcode=b.hcode and ( a.`path` !=b.`path`
or a.filename !=b.filename ) limit 53000;

SELECT  f.systemdriver  FROM filedetails f GROUP BY f.systemdriver


SELECT COUNT(*)
FROM torr.filedetails  a,torr.filedetails_dup b where a.hcode=b.hcode limit 25000;


SELECT concat(a.systemdriver,a.path,'/',a.filename,a.filetype) as src,
concat(b.systemdriver,b.path,'/',b.filename,b.filetype) as dup,a.filesize ,b.filesize
FROM torr.filedetails  a,torr.filedetails_dup b where a.hcode=b.hcode and a.`path` =b.`path`
and a.filename =b.filename

SELECT count(*)
FROM torr.filedetails  a,torr.filedetails_dup b where a.hcode=b.hcode and a.`path` =b.`path`
and a.filename =b.filename


select * from filedetails f where hcode ='654253eb1e04ab830f00d8fcd73a2516'

select * from filedetails_dup fd  where hcode ='654253eb1e04ab830f00d8fcd73a2516'
