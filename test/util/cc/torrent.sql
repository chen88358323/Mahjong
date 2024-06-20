
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

----查询相同hcode

select f1.id,f1.hcode,f1.path,f1.filename,
f2.id,f2.hcode,f2.path,f2.filename
FROM torrents_dup f1
JOIN torrents_dup f2 ON f1.hcode = f2.hcode



	SELECT
    f1.id AS f1_id,
    f1.hcode AS f1_hcode,
    f1.path AS f1_path,
    f1.filename AS f1_filename,
    f2.id AS f2_id,
    f2.hcode AS f2_hcode,
    f2.path AS f2_path,
    f2.filename AS f2_filename
FROM
    torrents f1
JOIN
    torrents_dup f2
ON
    f1.hcode = f2.hcode order by f1_hcode

-----删除重复数据

select *
FROM torrents_dup f1
JOIN torrents_dup f2 ON f1.filename = f2.filename and  f1.path = f2.path AND f1.id != f2.id;


 (select f1.hcode,f1.id ,f1.path,f1.filename from torrents  f1
 where f1.filename like'%私拍%') union
(select f2.hcode,f2.id,f2.path,f2.filename from torrents_dup f2
where f2.filename like '%私拍%' )



delete from torrents where path like 'D:\\temp\\0555\\2022-03-01\\0555\\best10\\%'
delete from torrents_dup where path like 'D:\\temp\\0555\\2022-03-01\\0555\\best10\\%'


-----查询该目录下与之重复的文件列表
SELECT concat(a.path,'\\',a.filename) as src,
 concat(b.path,'\\',b.filename) as dup,
a.hcode,a.id ,b.id
FROM torr.torrents  a,torr.torrents_dup b
where (   a.hcode=b.hcode and
 a.path like '%b32%'   ) limit 1000;
