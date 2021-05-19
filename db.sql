-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               8.0.24 - MySQL Community Server - GPL
-- Server OS:                    Linux
-- HeidiSQL Version:             11.2.0.6213
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for movies
CREATE DATABASE IF NOT EXISTS `movies` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `movies`;

-- Dumping structure for table movies.genres
CREATE TABLE IF NOT EXISTS `genres` (
  `id` char(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '',
  `name` char(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table movies.genres: ~2 rows (approximately)
/*!40000 ALTER TABLE `genres` DISABLE KEYS */;
INSERT INTO `genres` (`id`, `name`) VALUES
	('ADV', 'Adventure'),
	('ANI', 'Animation'),
	('COM', 'Comedy');
/*!40000 ALTER TABLE `genres` ENABLE KEYS */;

-- Dumping structure for table movies.movie
CREATE TABLE IF NOT EXISTS `movie` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` text,
  `director` text,
  `length` int DEFAULT '0',
  `date` date DEFAULT NULL,
  `like` int DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table movies.movie: ~0 rows (approximately)
/*!40000 ALTER TABLE `movie` DISABLE KEYS */;
INSERT INTO `movie` (`id`, `name`, `director`, `length`, `date`, `like`) VALUES
	(1, 'The Mitchells vs. the Machines', 'Michael Rianda', 113, '2021-04-30', 0);
/*!40000 ALTER TABLE `movie` ENABLE KEYS */;

-- Dumping structure for table movies.movie_genres
CREATE TABLE IF NOT EXISTS `movie_genres` (
  `movie_id` int NOT NULL,
  `genres` char(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '',
  PRIMARY KEY (`movie_id`,`genres`) USING BTREE,
  KEY `FK_geners_geners` (`genres`) USING BTREE,
  CONSTRAINT `FK_genres_genres` FOREIGN KEY (`genres`) REFERENCES `genres` (`id`),
  CONSTRAINT `FK_movie_id_movie_id` FOREIGN KEY (`movie_id`) REFERENCES `movie` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table movies.movie_genres: ~2 rows (approximately)
/*!40000 ALTER TABLE `movie_genres` DISABLE KEYS */;
INSERT INTO `movie_genres` (`movie_id`, `genres`) VALUES
	(1, 'ADV'),
	(1, 'ANI'),
	(1, 'COM');
/*!40000 ALTER TABLE `movie_genres` ENABLE KEYS */;

-- Dumping structure for view movies.view_movie_genres
-- Creating temporary table to overcome VIEW dependency errors
CREATE TABLE `view_movie_genres` (
	`id` INT(10) NOT NULL,
	`name` TEXT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`director` TEXT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`length` INT(10) NULL,
	`date` DATE NULL,
	`like` INT(10) NULL,
	`genres` CHAR(50) NULL COLLATE 'utf8mb4_0900_ai_ci'
) ENGINE=MyISAM;

-- Dumping structure for view movies.view_movie_genres
-- Removing temporary table and create final VIEW structure
DROP TABLE IF EXISTS `view_movie_genres`;
CREATE ALGORITHM=UNDEFINED SQL SECURITY DEFINER VIEW `view_movie_genres` AS select `movie`.`id` AS `id`,`movie`.`name` AS `name`,`movie`.`director` AS `director`,`movie`.`length` AS `length`,`movie`.`date` AS `date`,`movie`.`like` AS `like`,`genres`.`name` AS `genres` from ((`movie_genres` `mg` join `movie` on((`mg`.`movie_id` = `movie`.`id`))) join `genres` on((`mg`.`genres` = `genres`.`id`)));

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
