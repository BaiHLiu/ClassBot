-- phpMyAdmin SQL Dump
-- version 4.9.5
-- https://www.phpmyadmin.net/
--
-- 主机： localhost
-- 生成日期： 2021-03-07 15:29:46
-- 服务器版本： 5.6.50-log
-- PHP 版本： 7.2.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 数据库： `qqbot`
--

-- --------------------------------------------------------

--
-- 表的结构 `CA_project`
--

CREATE TABLE `CA_project` (
  `id` int(5) NOT NULL,
  `title` varchar(50) NOT NULL,
  `description` varchar(200) NOT NULL,
  `date` date NOT NULL COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='班级事项提醒_项目信息';

-- --------------------------------------------------------

--
-- 表的结构 `CA_submit`
--

CREATE TABLE `CA_submit` (
  `sid` int(8) NOT NULL,
  `username` varchar(10) NOT NULL,
  `pid` int(11) NOT NULL COMMENT '项目id',
  `stime` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='班级事项提醒_提交记录';

-- --------------------------------------------------------

--
-- 表的结构 `CA_userinfo`
--

CREATE TABLE `CA_userinfo` (
  `uid` int(5) NOT NULL,
  `user_id` varchar(12) NOT NULL COMMENT 'QQ号',
  `user_name` varchar(20) NOT NULL,
  `user_class` varchar(30) NOT NULL,
  `alert_count` int(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='班级事项提醒_成员信息';

-- --------------------------------------------------------

--
-- 表的结构 `CZ_imginfo`
--

CREATE TABLE `CZ_imginfo` (
  `imgid` int(8) NOT NULL,
  `file_name` varchar(50) NOT NULL COMMENT '图片文件名',
  `user_id` varchar(12) NOT NULL COMMENT '发图人qq号',
  `upload_date` date NOT NULL COMMENT '发图日期',
  `upload_time` time NOT NULL COMMENT '发图时间',
  `ocr_err_code` int(2) NOT NULL,
  `ocr_times` varchar(5) NOT NULL,
  `ocr_scores` varchar(8) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='重走长征路截图上传_图片信息';

-- --------------------------------------------------------

--
-- 表的结构 `userinfo`
--

CREATE TABLE `userinfo` (
  `uid` int(5) NOT NULL,
  `user_id` varchar(12) NOT NULL COMMENT 'QQ号',
  `user_name` varchar(20) NOT NULL,
  `user_class` varchar(30) NOT NULL,
  `last_cmd` varchar(50) NOT NULL COMMENT '最近一条命令',
  `last_upload_date` date NOT NULL,
  `last_upload_time` time NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='注册用户信息';

--
-- 转储表的索引
--

--
-- 表的索引 `CA_project`
--
ALTER TABLE `CA_project`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `CA_submit`
--
ALTER TABLE `CA_submit`
  ADD PRIMARY KEY (`sid`);

--
-- 表的索引 `CA_userinfo`
--
ALTER TABLE `CA_userinfo`
  ADD PRIMARY KEY (`uid`);

--
-- 表的索引 `CZ_imginfo`
--
ALTER TABLE `CZ_imginfo`
  ADD PRIMARY KEY (`imgid`);

--
-- 表的索引 `userinfo`
--
ALTER TABLE `userinfo`
  ADD PRIMARY KEY (`uid`);

--
-- 在导出的表使用AUTO_INCREMENT
--

--
-- 使用表AUTO_INCREMENT `CA_project`
--
ALTER TABLE `CA_project`
  MODIFY `id` int(5) NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `CA_submit`
--
ALTER TABLE `CA_submit`
  MODIFY `sid` int(8) NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `CA_userinfo`
--
ALTER TABLE `CA_userinfo`
  MODIFY `uid` int(5) NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `CZ_imginfo`
--
ALTER TABLE `CZ_imginfo`
  MODIFY `imgid` int(8) NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `userinfo`
--
ALTER TABLE `userinfo`
  MODIFY `uid` int(5) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
