--
-- ���� ������������ � ������� SQLiteStudio v3.4.13 � �� ��� 28 03:55:44 2025
--
-- �������������� ��������� ������: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- �������: characters_stats
CREATE TABLE IF NOT EXISTS characters_stats (id INTEGER PRIMARY KEY UNIQUE, name TEXT, name_file TEXT, health_min INTEGER, health_max INTEGER, damage_min INTEGER, damage_max INTEGER, protect_min INTEGER, protect_max INTEGER, energy_min INTEGER, energy_max INTEGER, luck_min INTEGER, luck_max INTEGER);
INSERT INTO characters_stats (id, name, name_file, health_min, health_max, damage_min, damage_max, protect_min, protect_max, energy_min, energy_max, luck_min, luck_max) VALUES (31, 'Mage', 'mage_texture', 50, 150, 7, 15, 1, 3, 50, 70, 1, 10);

-- �������: enemies_stats
CREATE TABLE IF NOT EXISTS enemies_stats (id INTEGER PRIMARY KEY UNIQUE, name TEXT, name_file TEXT, health_min INTEGER, health_max INTEGER, damage_min INTEGER, damage_max INTEGER, protect_min INTEGER, protect_max INTEGER);
INSERT INTO enemies_stats (id, name, name_file, health_min, health_max, damage_min, damage_max, protect_min, protect_max) VALUES (40, '�����', 'daemon', 65, 85, 10, 16, 2, 4);
INSERT INTO enemies_stats (id, name, name_file, health_min, health_max, damage_min, damage_max, protect_min, protect_max) VALUES (41, '���������', 'werewolf', 70, 90, 8, 14, 3, 5);
INSERT INTO enemies_stats (id, name, name_file, health_min, health_max, damage_min, damage_max, protect_min, protect_max) VALUES (42, '������', 'vampire', 40, 200, 4, 8, 2, 3);

-- �������: items1
CREATE TABLE IF NOT EXISTS items1 (id INTEGER PRIMARY KEY UNIQUE, name TEXT, name_file TEXT, health_min INTEGER, health_max INTEGER, damage_min INTEGER, damage_max INTEGER, protect_min INTEGER, protect_max INTEGER, energy_min INTEGER, energy_max INTEGER, luck_min INTEGER, luck_max INTEGER);
INSERT INTO items1 (id, name, name_file, health_min, health_max, damage_min, damage_max, protect_min, protect_max, energy_min, energy_max, luck_min, luck_max) VALUES (50, '������� ��������', 'red_cr', 5, 7, 0, 1, 0, 1, 1, 3, 0, 1);
INSERT INTO items1 (id, name, name_file, health_min, health_max, damage_min, damage_max, protect_min, protect_max, energy_min, energy_max, luck_min, luck_max) VALUES (51, '����� ��������', 'blue_cr', 0, 2, 0, 1, 0, 4, 5, 7, 0, 1);
INSERT INTO items1 (id, name, name_file, health_min, health_max, damage_min, damage_max, protect_min, protect_max, energy_min, energy_max, luck_min, luck_max) VALUES (52, '������� ��������', 'green_cr', 0, 1, 0, 2, 1, 3, 0, 1, 1, 4);
INSERT INTO items1 (id, name, name_file, health_min, health_max, damage_min, damage_max, protect_min, protect_max, energy_min, energy_max, luck_min, luck_max) VALUES (53, '���������� ��������', 'purple_cr', 0, 1, 5, 7, 0, 1, 1, 2, 0, 1);

-- �������: items2
CREATE TABLE IF NOT EXISTS items2 (id INTEGER PRIMARY KEY UNIQUE, name TEXT, name_file TEXT, health_min INTEGER, health_max INTEGER, damage_min INTEGER, damage_max INTEGER, protect_min INTEGER, protect_max INTEGER, energy_min INTEGER, energy_max INTEGER, luck_min INTEGER, luck_max INTEGER);
INSERT INTO items2 (id, name, name_file, health_min, health_max, damage_min, damage_max, protect_min, protect_max, energy_min, energy_max, luck_min, luck_max) VALUES (70, '����', 'helmet', 0, 0, 0, 0, 3, 5, 0, 0, 0, 0);
INSERT INTO items2 (id, name, name_file, health_min, health_max, damage_min, damage_max, protect_min, protect_max, energy_min, energy_max, luck_min, luck_max) VALUES (71, '���', 'sword', 0, 0, 4, 7, 0, 0, 0, 0, 0, 0);
INSERT INTO items2 (id, name, name_file, health_min, health_max, damage_min, damage_max, protect_min, protect_max, energy_min, energy_max, luck_min, luck_max) VALUES (72, '���', 'bow', 0, 0, 3, 6, 0, 0, 0, 0, 0, 0);
INSERT INTO items2 (id, name, name_file, health_min, health_max, damage_min, damage_max, protect_min, protect_max, energy_min, energy_max, luck_min, luck_max) VALUES (73, '�������', 'armor', 0, 0, 0, 0, 4, 7, 0, 0, 0, 0);
INSERT INTO items2 (id, name, name_file, health_min, health_max, damage_min, damage_max, protect_min, protect_max, energy_min, energy_max, luck_min, luck_max) VALUES (74, '���', 'knife', 0, 0, 1, 5, 0, 0, 0, 0, 0, 0);
INSERT INTO items2 (id, name, name_file, health_min, health_max, damage_min, damage_max, protect_min, protect_max, energy_min, energy_max, luck_min, luck_max) VALUES (75, '���', 'shield', 0, 0, 0, 0, 1, 5, 0, 2, 0, 0);
INSERT INTO items2 (id, name, name_file, health_min, health_max, damage_min, damage_max, protect_min, protect_max, energy_min, energy_max, luck_min, luck_max) VALUES (76, '�����', 'magic_staff', 0, 0, 1, 2, 0, 0, 3, 8, 0, 0);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
