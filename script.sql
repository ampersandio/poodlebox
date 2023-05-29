-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema poodle_box
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema poodle_box
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `poodle_box` DEFAULT CHARACTER SET utf8mb4 ;
USE `poodle_box` ;

-- -----------------------------------------------------
-- Table `poodle_box`.`roles`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `poodle_box`.`roles` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `type` VARCHAR(45) NOT NULL,
    PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 1
DEFAULT CHARACTER SET = utf8mb4;

-- -----------------------------------------------------
-- Table `poodle_box`.`content_types`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `poodle_box`.`content_types` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `type` VARCHAR(45) NOT NULL,
    PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 1
DEFAULT CHARACTER SET = utf8mb4;
-- -----------------------------------------------------
-- Table `poodle_box`.`subscriptions`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `poodle_box`.`subscriptions` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `type` VARCHAR(45) NOT NULL,
    PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 1
DEFAULT CHARACTER SET = utf8mb4;

-- -----------------------------------------------------
-- Table `poodle_box`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `poodle_box`.`users` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(45) NOT NULL,
  `first_name` VARCHAR(45) NOT NULL,
  `last_name` VARCHAR(45) NOT NULL,
  `password` VARCHAR(200) NOT NULL,
  `phone_number` VARCHAR(45),
  `date_of_birth` DATE NOT NULL,
  `verified_email` TINYINT(4) NOT NULL,
  `approved` TINYINT(4),
  `role` INT(11) NOT NULL,
  `linked_in_profile` VARCHAR(200),
  `disabled` TINYINT(4) NOT NULL,
  `profile_picture` VARCHAR(200),
  PRIMARY KEY (`id`),
  INDEX `fk_users_roles1_idx` (`role` ASC) ,
  CONSTRAINT `fk_users_roles1`
    FOREIGN KEY (`role`)
    REFERENCES `poodle_box`.`roles` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  UNIQUE INDEX `email_UNIQUE` (`email` ASC))
  
ENGINE = InnoDB
AUTO_INCREMENT = 1
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `poodle_box`.`courses`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `poodle_box`.`courses` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(45) NOT NULL,
  `description` LONGTEXT NOT NULL,
  `objectives` LONGTEXT NOT NULL,
  `premium` TINYINT(4) NOT NULL,
  `active` TINYINT(4) NOT NULL,
  `owner` INT(11) NOT NULL,
  `price` FLOAT(11),
  `course_picture` VARCHAR(200),
  PRIMARY KEY (`id`),
  INDEX `fk_courses_users1_idx` (`owner` ASC) ,
  CONSTRAINT `fk_courses_users1`
    FOREIGN KEY (`owner`)
    REFERENCES `poodle_box`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  UNIQUE INDEX `title_UNIQUE` (`title` ASC) )
ENGINE = InnoDB
AUTO_INCREMENT = 1
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `poodle_box`.`sections`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `poodle_box`.`sections` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(45) NOT NULL,
  `courses_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_sections_courses1_idx` (`courses_id` ASC) ,
  CONSTRAINT `fk_sections_courses1`
    FOREIGN KEY (`courses_id`)
    REFERENCES `poodle_box`.`courses` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  UNIQUE INDEX `title_UNIQUE` (`title` ASC) )  
ENGINE = InnoDB
AUTO_INCREMENT = 1
DEFAULT CHARACTER SET = utf8mb4;

-- -----------------------------------------------------
-- Table `poodle_box`.`content`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `poodle_box`.`content` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(45) NOT NULL,
  `description` LONGTEXT,
  `content_types_id` INT(11) NOT NULL,
  `sections_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_content_sections1_idx` (`sections_id` ASC) ,
  CONSTRAINT `fk_content_sections1`
    FOREIGN KEY (`sections_id`)
    REFERENCES `poodle_box`.`sections` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  INDEX `fk_content_content_types1_idx` (`content_types_id` ASC) ,
  CONSTRAINT `fk_content_content_types_id1`
    FOREIGN KEY (`content_types_id`)
    REFERENCES `poodle_box`.`content_types` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 1
DEFAULT CHARACTER SET = utf8mb4;

-- -----------------------------------------------------
-- Table `poodle_box`.`tags`
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS `poodle_box`.`tags` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `name_UNIQUE` (`name` ASC) )
ENGINE = InnoDB
AUTO_INCREMENT = 1
DEFAULT CHARACTER SET = utf8mb4;

-- -----------------------------------------------------
-- Table `poodle_box`.`certificates`
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS `poodle_box`.`certificates` (
  `id` INT(11) NOT NULL,
  `users_id` INT(45) NOT NULL,
  `courses_id` INT(45) NOT NULL,
  `issued_date` DATE NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_certificates_courses1_idx` (`courses_id` ASC) ,
  INDEX `fk_certificates_users1_idx` (`users_id` ASC) ,
  CONSTRAINT `fk_certificates_users1`
    FOREIGN KEY (`users_id`)
    REFERENCES `poodle_box`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_certificates_courses1`
    FOREIGN KEY (`courses_id`)
    REFERENCES `poodle_box`.`courses` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)

ENGINE = InnoDB
AUTO_INCREMENT = 1
DEFAULT CHARACTER SET = utf8mb4;



-- -----------------------------------------------------
-- Table `poodle_box`.`tags_has_courses`
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS `poodle_box`.`tags_has_courses` (
  `courses_id` INT(11) NOT NULL,
  `tags_id` INT(11) NOT NULL,
  PRIMARY KEY (`courses_id`, `tags_id`),
  INDEX `fk_tags_has_courses_courses1_idx` (`courses_id` ASC) ,
  INDEX `fk_tags_has_courses_tags1_idx` (`tags_id` ASC) ,
  CONSTRAINT `fk_tags_has_courses_tags1`
    FOREIGN KEY (`tags_id`)
    REFERENCES `poodle_box`.`tags` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_tags_has_courses_courses1`
    FOREIGN KEY (`courses_id`)
    REFERENCES `poodle_box`.`courses` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;

-- -----------------------------------------------------
-- Table `poodle_box`.`interests`
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS `poodle_box`.`interests` (
  `users_id` INT(11) NOT NULL,
  `tags_id` INT(11) NOT NULL,
  `relevance` INT(11) NOT NULL,
  PRIMARY KEY (`users_id`, `tags_id`),
  INDEX `fk_interests_courses1_idx` (`users_id` ASC) ,
  INDEX `fk_interests_tags1_idx` (`tags_id` ASC) ,
  CONSTRAINT `fk_interests_tags1`
    FOREIGN KEY (`tags_id`)
    REFERENCES `poodle_box`.`tags` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_interests_courses1`
    FOREIGN KEY (`users_id`)
    REFERENCES `poodle_box`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;
-- -----------------------------------------------------
-- Table `poodle_box`.`reviews`
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS `poodle_box`.`reviews` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `users_id` INT(11) NOT NULL,
  `courses_id` INT(11) NOT NULL,
  `rating` DOUBLE NOT NULL,
  `description` LONGTEXT ,
  PRIMARY KEY (`id`),
  INDEX `fk_reviews_courses1_idx` (`courses_id` ASC) ,
  INDEX `fk_reviews_users1_idx` (`users_id` ASC) ,
  CONSTRAINT `fk_reviews_courses1`
    FOREIGN KEY (`courses_id`)
    REFERENCES `poodle_box`.`courses` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_reviews_users1`
    FOREIGN KEY (`users_id`)
    REFERENCES `poodle_box`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 1
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `poodle_box`.`users_has_courses`
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS `poodle_box`.`users_has_courses` (
  `users_id` INT(11) NOT NULL,
  `courses_id` INT(11) NOT NULL,
  `subscriptions_id` INT(4) NOT NULL,
  PRIMARY KEY (`courses_id`, `users_id`,`subscriptions_id`),
  INDEX `fk_users_has_courses_courses1_idx` (`courses_id` ASC) ,
  INDEX `fk_users_has_courses_users1_idx` (`users_id` ASC) ,
  INDEX `fk_users_has_courses_subscriptions1_idx` (`subscriptions_id` ASC) ,
  CONSTRAINT `fk_users_has_courses_courses1`
    FOREIGN KEY (`courses_id`)
    REFERENCES `poodle_box`.`courses` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_has_courses_users1`
    FOREIGN KEY (`users_id`)
    REFERENCES `poodle_box`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_has_courses_subscriptions1`
    FOREIGN KEY (`subscriptions_id`)
    REFERENCES `poodle_box`.`subscriptions` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;

-- -----------------------------------------------------
-- Table `poodle_box`.`users_has_sections`
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS `poodle_box`.`users_has_sections` (
  `users_id` INT(11) NOT NULL,
  `sections_id` INT(11) NOT NULL,
  PRIMARY KEY (`users_id`, `sections_id`),
  INDEX `fk_users_has_courses_sections1_idx` (`sections_id` ASC) ,
  INDEX `fk_users_has_courses_users1_idx` (`users_id` ASC) ,
  CONSTRAINT `fk_users_has_sections_sections1`
    FOREIGN KEY (`sections_id`)
    REFERENCES `poodle_box`.`sections` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_has_sections1`
    FOREIGN KEY (`users_id`)
    REFERENCES `poodle_box`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;