-- MySQL dump 10.13  Distrib 8.0.34, for Linux (x86_64)
--
-- Host: localhost    Database: pfadi
-- ------------------------------------------------------
-- Server version	8.0.34-0ubuntu0.22.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) COLLATE utf8mb3_bin NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('477a62eae029');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pfadikind`
--

DROP TABLE IF EXISTS `pfadikind`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pfadikind` (
  `id` int NOT NULL AUTO_INCREMENT,
  `pfadiname` varchar(64) COLLATE utf8mb3_bin DEFAULT NULL,
  `vegetarisch` tinyint(1) DEFAULT NULL,
  `vorname` varchar(64) COLLATE utf8mb3_bin DEFAULT NULL,
  `nachname` varchar(64) COLLATE utf8mb3_bin DEFAULT NULL,
  `geburtsdatum` date DEFAULT NULL,
  `adresse` varchar(128) COLLATE utf8mb3_bin DEFAULT NULL,
  `telefonprivat` varchar(20) COLLATE utf8mb3_bin DEFAULT NULL,
  `telefonberuflich` varchar(20) COLLATE utf8mb3_bin DEFAULT NULL,
  `allergien_unvertraeglichkeiten` text COLLATE utf8mb3_bin,
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `pfadikind_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pfadikind`
--

LOCK TABLES `pfadikind` WRITE;
/*!40000 ALTER TABLE `pfadikind` DISABLE KEYS */;
INSERT INTO `pfadikind` VALUES (1,'Spider',1,'Miles','Parcker','2010-10-10','Züricherstrasse 15, 8004, Zürich','044 111 11 11','079 666 66 66','Erdnussallergie\r\n',2),(2,'Zoro',0,'Adi','Mustermann','2015-05-10','Josefstrasse 155, 8005 Zurüch','041 748 32 01','079 999 99 99','Gemüsse ',3),(3,'Ruffi',1,'David','Mustermann','2010-05-01','Josefstrasse 155, 8005 Zurüch','041 748 32 01','079 999 99 99','Keine',3);
/*!40000 ALTER TABLE `pfadikind` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pfadilager`
--

DROP TABLE IF EXISTS `pfadilager`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pfadilager` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb3_bin NOT NULL,
  `datum` varchar(50) COLLATE utf8mb3_bin NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pfadilager`
--

LOCK TABLES `pfadilager` WRITE;
/*!40000 ALTER TABLE `pfadilager` DISABLE KEYS */;
INSERT INTO `pfadilager` VALUES (1,'ChlaWe (Chlaus-Weekend)','Dezember 2023'),(2,'Pfila (Pfingst-Lager)','Mai 2023'),(3,'SoLa (Sommer-Lager) ','Jul 2023'),(4,'HeLa (Herbst-Lager)','Okt 2023');
/*!40000 ALTER TABLE `pfadilager` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pfadilageranmeldung`
--

DROP TABLE IF EXISTS `pfadilageranmeldung`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pfadilageranmeldung` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `pfadilager_id` int NOT NULL,
  `datum` varchar(50) COLLATE utf8mb3_bin NOT NULL,
  `vorname` varchar(64) COLLATE utf8mb3_bin DEFAULT NULL,
  `nachname` varchar(64) COLLATE utf8mb3_bin DEFAULT NULL,
  `pfadikind_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `pfadikind_id` (`pfadikind_id`),
  KEY `pfadilager_id` (`pfadilager_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `pfadilageranmeldung_ibfk_1` FOREIGN KEY (`pfadikind_id`) REFERENCES `pfadikind` (`id`),
  CONSTRAINT `pfadilageranmeldung_ibfk_2` FOREIGN KEY (`pfadilager_id`) REFERENCES `pfadilager` (`id`),
  CONSTRAINT `pfadilageranmeldung_ibfk_3` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pfadilageranmeldung`
--

LOCK TABLES `pfadilageranmeldung` WRITE;
/*!40000 ALTER TABLE `pfadilageranmeldung` DISABLE KEYS */;
INSERT INTO `pfadilageranmeldung` VALUES (5,3,2,'Mai 2023','Adi','Mustermann',2),(6,3,1,'Dezember 2023','David','Mustermann',3);
/*!40000 ALTER TABLE `pfadilageranmeldung` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(64) COLLATE utf8mb3_bin DEFAULT NULL,
  `vorname` varchar(64) COLLATE utf8mb3_bin DEFAULT NULL,
  `nachname` varchar(64) COLLATE utf8mb3_bin DEFAULT NULL,
  `email` varchar(120) COLLATE utf8mb3_bin DEFAULT NULL,
  `password_hash` varchar(128) COLLATE utf8mb3_bin DEFAULT NULL,
  `role` varchar(64) COLLATE utf8mb3_bin DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_user_email` (`email`),
  UNIQUE KEY `ix_user_username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'adminan','Andrej','Administrator','admin@admin.ch','pbkdf2:sha256:600000$Q3dMHUcs08CoJr4m$ba3c6f7be515098c0185bfb7b42bf857b05e034e6356620153b3204a58b6458a','admin'),(2,'p.parcker','Peter ','Parcker','peter@parker.ch','pbkdf2:sha256:600000$MWJWnq4emMdXtcKK$f67c6308ab7f3e900afca16f3d0d703db71aed185e5f34d0b17431443d59e460','user'),(3,'max','Max','Mustermann','max.msutermann@google.ch','pbkdf2:sha256:600000$JgatfnBGQ0aWlAwG$2cfaddfe50259f33f6ce9ea38c3cb6dedf9e0c8f14ab9924250fb234f4b7d97c','user');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-08-31 20:50:26
