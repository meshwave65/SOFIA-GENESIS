-- Script de Criação do Banco de Dados: sofia_db
-- Arquitetura: v3.0

CREATE DATABASE IF NOT EXISTS sofia_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE sofia_db;

-- Tabela 1: tasks - O coração do sistema.
CREATE TABLE `tasks` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `title` VARCHAR(255) NOT NULL,
  `description` TEXT,
  `status` ENUM('pending', 'in_progress', 'managing', 'on_hold', 'completed', 'cancelled') NOT NULL DEFAULT 'pending',
  `priority` ENUM('critical', 'high', 'medium', 'low') NOT NULL DEFAULT 'medium',
  `parent_task_id` INT NULL COMMENT 'ID da Tarefa Pai (Auto-relacionamento)',
  `wbs_tag` VARCHAR(50) NULL COMMENT 'A "Metatag" Hierárquica (ex: 234)',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT `fk_parent_task` FOREIGN KEY (`parent_task_id`) REFERENCES `tasks`(`id`) ON DELETE SET NULL
) ENGINE=InnoDB;

-- Tabela 2: metadata_types - A "paleta" de tipos de etiquetas.
CREATE TABLE `metadata_types` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(100) NOT NULL UNIQUE COMMENT 'Ex: agent_specialization, project_context'
) ENGINE=InnoDB;

-- Tabela 3: metadata_values - Os valores possíveis para cada tipo de etiqueta.
CREATE TABLE `metadata_values` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `type_id` INT NOT NULL,
  `value` VARCHAR(255) NOT NULL,
  CONSTRAINT `fk_metadata_type` FOREIGN KEY (`type_id`) REFERENCES `metadata_types`(`id`) ON DELETE CASCADE,
  UNIQUE KEY `type_value_unique` (`type_id`, `value`)
) ENGINE=InnoDB;

-- Tabela 4: task_metadata - A tabela de junção que conecta tarefas a suas etiquetas.
CREATE TABLE `task_metadata` (
  `task_id` INT NOT NULL,
  `metadata_id` INT NOT NULL,
  PRIMARY KEY (`task_id`, `metadata_id`),
  CONSTRAINT `fk_task_meta_task` FOREIGN KEY (`task_id`) REFERENCES `tasks`(`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_task_meta_value` FOREIGN KEY (`metadata_id`) REFERENCES `metadata_values`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Tabela 5: task_history - O log imutável de tudo que acontece com uma tarefa.
CREATE TABLE `task_history` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `task_id` INT NOT NULL,
  `timestamp` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `author_id` VARCHAR(100),
  `event_type` ENUM('created', 'status_change', 'comment', 'assignment', 'metadata_change', 'desmembered') NOT NULL,
  `details` JSON,
  CONSTRAINT `fk_history_task` FOREIGN KEY (`task_id`) REFERENCES `tasks`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB;


