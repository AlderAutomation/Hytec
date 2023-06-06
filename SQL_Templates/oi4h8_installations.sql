-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jun 06, 2023 at 02:07 PM
-- Server version: 10.3.39-MariaDB
-- PHP Version: 8.1.16

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `myhytec_dotcomdb`
--

-- --------------------------------------------------------

--
-- Table structure for table `oi4h8_installations`
--

CREATE TABLE `oi4h8_installations` (
  `installation_id` int(11) NOT NULL,
  `sites_site_id` int(11) NOT NULL,
  `device_serial_num` varchar(45) NOT NULL,
  `company_id` varchar(100) DEFAULT NULL,
  `alarm_code` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `oi4h8_installations`
--

INSERT INTO `oi4h8_installations` (`installation_id`, `sites_site_id`, `device_serial_num`, `company_id`, `alarm_code`) VALUES
(1, 1, '1510050448', 'PROMAG ENVIRO SYSTEMS LTD', ''),
(24, 13, '1602254153', 'PROMAG ENVIRO SYSTEMS LTD', ''),
(25, 14, '1510070718', 'PROMAG ENVIRO SYSTEMS LTD', ''),
(26, 15, '1510070717', 'PROMAG ENVIRO SYSTEMS LTD', ''),
(27, 16, '1510070716', 'PROMAG ENVIRO SYSTEMS LTD', ''),
(28, 16, '1601070650', 'PROMAG ENVIRO SYSTEMS LTD', ''),
(29, 17, '1234', NULL, NULL),
(30, 18, '234543456', NULL, NULL),
(31, 18, '', NULL, ''),
(32, 19, '1602254152', 'PROMAG ENVIRO SYSTEMS LTD', ''),
(35, 20, '1602122083', 'Promag Master Account', ''),
(36, 21, '1602122098', 'Promag Master Account', ''),
(37, 22, '1605111796', 'PROMAG ENVIRO SYSTEMS LTD', ''),
(38, 23, '1905210923', 'Promag Master Account', ''),
(39, 24, '1602254151', 'Promag Master Account', ''),
(42, 26, '1602122097', NULL, NULL),
(43, 27, '1604121527', 'Promag Master Account', ''),
(44, 28, '1605111793', NULL, NULL),
(46, 30, '1602122096', 'Promag Master Account', ''),
(47, 31, '1609132084', 'Promag Master Account', ''),
(48, 44, '1807180774', 'Promag Master Account', ''),
(53, 65, '1606071150', 'Promag Master Account', ''),
(54, 105, '1509254083', 'Promag Master Account', ''),
(55, 115, '1602122079', 'Promag Master Account', 'AquaSoft (S11) High Alarm'),
(56, 115, '1602122080', 'Promag Master Account', ''),
(57, 125, '1609132082', 'Promag Master Account', ''),
(58, 131, '1602254150', 'Promag Master Account', ''),
(59, 131, '1602122077', 'Promag Master Account', ''),
(60, 140, '1607264384', 'Promag Master Account', ''),
(61, 141, '1606071152', 'Promag Master Account', ''),
(62, 142, '1602040747', 'Promag Master Account', ''),
(63, 150, '1609132076', NULL, NULL),
(64, 171, '1607264385', 'Promag Master Account', ''),
(65, 175, '1602122099', 'Promag Master Account', ''),
(66, 54, '1605111795', 'Promag Master Account', ''),
(67, 180, '1609132077', 'Promag Master Account', ''),
(68, 33, '1902200801', 'Promag Master Account', ''),
(70, 183, '1608172957', 'Promag Master Account', 'pH (S21) High Alarm'),
(71, 184, '1611305320', NULL, NULL),
(72, 184, '1611183617', NULL, NULL),
(74, 215, '1611183619', NULL, NULL),
(75, 215, '1611183616', NULL, NULL),
(76, 215, '1611183620', NULL, NULL),
(77, 228, '1701050012', 'Promag Master Account', ''),
(78, 230, '1605111794', 'Promag Master Account', ''),
(79, 233, '1602122101', 'Promag Master Account', ''),
(80, 235, '1609132083', 'Promag Master Account', ''),
(81, 242, '1609132080', 'Promag Master Account', ''),
(82, 75, '1612204235', 'Promag Master Account', ''),
(83, 243, '1609234064', 'Promag Master Account', 'ORP (S11) Low Alarm'),
(84, 244, '1611183612', NULL, NULL),
(85, 248, '1605111790', 'Promag Master Account', 'pH (S21) High Alarm'),
(86, 252, '1605183030', 'Promag Master Account', ''),
(87, 255, '1612214444', 'Promag Master Account', ''),
(88, 256, '1701050011', 'Promag Master Account', ''),
(89, 263, '1611183614', 'Promag Master Account', ''),
(90, 61, '1608172954', 'Promag Master Account', ''),
(91, 267, '1606071151', NULL, NULL),
(92, 272, '1602122081', NULL, NULL),
(93, 273, '1611183610', NULL, NULL),
(94, 284, '1611183618', 'Promag Master Account', ''),
(95, 133, '1510070715', 'Promag Master Account', ''),
(96, 122, '1601152634', 'Promag Master Account', 'Flowswitch (D4) No Flow'),
(97, 159, '1609132079', 'Promag Master Account', ''),
(98, 91, '1701050010', 'Promag Master Account', ''),
(99, 92, '1703140571', NULL, NULL),
(100, 305, '1605111792', 'Promag Master Account', ''),
(101, 305, '1608172953', 'Promag Master Account', ''),
(102, 305, '1608172955', 'Promag Master Account', ''),
(103, 305, '1608315810', 'Promag Master Account', 'pH (S21) High Alarm'),
(104, 306, '1611183613', 'Promag Master Account', ''),
(105, 313, '1704190782', 'Promag Master Account', ''),
(106, 210, '1611183621', NULL, NULL),
(107, 258, '1606224215', NULL, NULL),
(108, 321, '1705180812', 'Promag Master Account', ''),
(109, 129, '1705180811', 'Promag Master Account', ''),
(110, 325, '1703140575', 'Promag Master Account', ''),
(111, 285, '1704030023', NULL, NULL),
(112, 328, '1701050008', 'Promag Master Account', ''),
(113, 329, '1705301239', 'Promag Master Account', ''),
(114, 330, '1705301243', 'Promag Master Account', ''),
(115, 331, '1705170749', 'Promag Master Account', ''),
(116, 311, '1705220903', 'Promag Master Account', 'pH (S21) High Alarm'),
(118, 67, '1705301237', 'Promag Master Account', ''),
(119, 317, '1601070651', 'Promag Master Account', ''),
(120, 332, '1708110437', 'Promag Master Account', ''),
(121, 233, '1708180654', 'Promag Master Account', ''),
(122, 233, '1705301241', 'Promag Master Account', ''),
(123, 151, '1605111791', 'Promag Master Account', ''),
(124, 104, '1704030021', 'Promag Master Account', ''),
(125, 334, '1708020105', 'Promag Master Account', ''),
(126, 335, '1708180653', 'Promag Master Account', 'Flowmeter (D1) High Alarm'),
(127, 293, '1702080240', 'Promag Master Account', 'pH (S21) High Alarm'),
(128, 336, '1705301235', 'Promag Master Account', 'Flowswitch (D4) No Flow'),
(129, 337, '1702280970', 'Promag Master Account', ''),
(130, 338, '1702080241', 'Promag Master Account', ''),
(131, 339, '1705301236', 'Promag Master Account', ''),
(132, 340, '1705301238', 'Promag Master Account', ''),
(133, 341, '1705170751', 'Promag Master Account', 'Temp (S22) Sensor Fault'),
(134, 342, '1703140568', 'Promag Master Account', '');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `oi4h8_installations`
--
ALTER TABLE `oi4h8_installations`
  ADD PRIMARY KEY (`installation_id`,`sites_site_id`),
  ADD UNIQUE KEY `device_serial_num_UNIQUE` (`device_serial_num`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `oi4h8_installations`
--
ALTER TABLE `oi4h8_installations`
  MODIFY `installation_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=551;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
