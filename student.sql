-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Mar 20, 2021 at 04:36 PM
-- Server version: 5.7.31
-- PHP Version: 7.3.21

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `student`
--

-- --------------------------------------------------------

--
-- Table structure for table `administrators`
--

DROP TABLE IF EXISTS `administrators`;
CREATE TABLE IF NOT EXISTS `administrators` (
  `idadministrators` int(11) NOT NULL,
  `password` varchar(45) NOT NULL,
  `username` varchar(45) NOT NULL,
  `User_name` varchar(300) NOT NULL,
  PRIMARY KEY (`idadministrators`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `administrators`
--

INSERT INTO `administrators` (`idadministrators`, `password`, `username`, `User_name`) VALUES
(6, 'Lec123', 'Albus Dumbledore', 'dumbledore.59'),
(7, 'Lec123', 'Minerva McGonagall', 'mcGonagall.63'),
(8, 'Lec123', 'Severus Snape', 'snape.68'),
(9, 'Lec123', 'Rubeus Hagrid', 'hagrid.60'),
(10, 'Lec123', 'Gilderoy Lockhart', 'lockhart.69');

-- --------------------------------------------------------

--
-- Table structure for table `applications`
--

DROP TABLE IF EXISTS `applications`;
CREATE TABLE IF NOT EXISTS `applications` (
  `idapplications` int(11) NOT NULL,
  `request_status` tinyint(4) DEFAULT NULL,
  `Details` text,
  `evidence` longblob,
  `filename` varchar(300) NOT NULL,
  `from_id` int(11) NOT NULL,
  `to_id` int(11) NOT NULL,
  `requestType` varchar(45) NOT NULL,
  `date` char(20) NOT NULL,
  `studentReaded` char(1) NOT NULL,
  `staffReaded` char(1) NOT NULL,
  `required` char(1) NOT NULL,
  PRIMARY KEY (`idapplications`),
  KEY `from_id_idx` (`from_id`),
  KEY `to_id_idx` (`to_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `comments`
--

DROP TABLE IF EXISTS `comments`;
CREATE TABLE IF NOT EXISTS `comments` (
  `idComments` int(11) NOT NULL,
  `commentUserType` tinyint(1) NOT NULL,
  `content` text NOT NULL,
  `idThreads` int(11) NOT NULL,
  `dateTime` char(50) NOT NULL,
  PRIMARY KEY (`idComments`),
  KEY `threadID` (`idThreads`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `students`
--

DROP TABLE IF EXISTS `students`;
CREATE TABLE IF NOT EXISTS `students` (
  `idStudents` int(11) NOT NULL,
  `Password` varchar(45) NOT NULL,
  `StudentUsername` varchar(45) NOT NULL,
  `studentIndex` varchar(45) NOT NULL,
  `User_name` varchar(300) NOT NULL,
  PRIMARY KEY (`idStudents`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `students`
--

INSERT INTO `students` (`idStudents`, `Password`, `StudentUsername`, `studentIndex`, `User_name`) VALUES
(1, 'Pass123', 'Harry James Potter', '190100', 'potter.19'),
(2, 'Pass123', 'Ronald Weasley', '190101', 'ronald.19'),
(3, 'Pass123', 'Hermione Granger', '190102', 'hermione.19'),
(4, 'Pass123', 'Draco Malfoy', '190103', 'malfoy.19'),
(5, 'Pass123', 'Ginny Weasley', '190104', 'ginny.19');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `idUsers` int(11) NOT NULL,
  `UserName` varchar(45) NOT NULL,
  `UserPassword` varchar(45) NOT NULL,
  `UserType` tinyint(4) NOT NULL,
  `User_name` varchar(300) NOT NULL,
  PRIMARY KEY (`idUsers`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`idUsers`, `UserName`, `UserPassword`, `UserType`, `User_name`) VALUES
(1, 'Harry James Potter', 'Pass123', 1, 'potter.19'),
(2, 'Ronald Weasley', 'Pass123', 1, 'ronald.19'),
(3, 'Hermione Granger', 'Pass123', 1, 'hermione.19'),
(4, 'Draco Malfoy', 'Pass123', 1, 'malfoy.19'),
(5, 'Ginny Weasley', 'Pass123', 1, 'ginny.19'),
(6, 'Albus Dumbledore', 'Lec123', 0, 'dumbledore.59'),
(7, 'Minerva McGonagall', 'Lec123', 0, 'mcGonagall.63'),
(8, 'Severus Snape', 'Lec123', 0, 'snape.68'),
(9, 'Rubeus Hagrid', 'Lec123', 0, 'hagrid.60'),
(10, 'Gilderoy Lockhart', 'Lec123', 0, 'lockhart.69');

--
-- Constraints for dumped tables
--

--
-- Constraints for table `applications`
--
ALTER TABLE `applications`
  ADD CONSTRAINT `from_id` FOREIGN KEY (`from_id`) REFERENCES `students` (`idStudents`),
  ADD CONSTRAINT `to_id` FOREIGN KEY (`to_id`) REFERENCES `administrators` (`idadministrators`);

--
-- Constraints for table `comments`
--
ALTER TABLE `comments`
  ADD CONSTRAINT `applicationId` FOREIGN KEY (`idThreads`) REFERENCES `applications` (`idapplications`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
