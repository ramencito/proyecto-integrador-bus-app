CREATE DATABASE UPBC_Bus_DB;
GO
USE UPBC_Bus_DB;
GO

--Tablas de datos
CREATE TABLE Rutas (id_ruta INT IDENTITY(1,1) PRIMARY KEY,nombre_corto VARCHAR(50) NOT NULL UNIQUE,nombre_completo VARCHAR(150) NOT NULL,trayecto VARCHAR(250) NOT NULL);
CREATE TABLE Horarios_Ruta (id_horario INT IDENTITY(1,1) PRIMARY KEY,id_ruta INT NOT NULL,turno VARCHAR(20) NOT NULL CHECK (turno IN ('matutino', 'vespertino')),
hora_llegada VARCHAR(5) NOT NULL, FOREIGN KEY (id_ruta) REFERENCES Rutas(id_ruta) ON DELETE CASCADE);
CREATE TABLE Coordenadas_Ruta (id_coordenada INT IDENTITY(1,1) PRIMARY KEY,id_ruta INT NOT NULL,secuencia INT NOT NULL,latitud FLOAT NOT NULL,
longitud FLOAT NOT NULL,FOREIGN KEY (id_ruta) REFERENCES Rutas(id_ruta) ON DELETE CASCADE);
GO

--Ponner tablas en rutas
INSERT INTO Rutas (nombre_corto, nombre_completo, trayecto) VALUES 
('amilpa', 'Ruta Cetys-Abasolo (Amilpa)', 'Zona Centro ➔ Cetys ➔ Campus UPBC'),
('violeta', 'Ruta 122 Santorales-UPBC (Violeta)', 'Santorales ➔ Lázaro Cárdenas ➔ UPBC');

-- Insertando horarios amilpa
DECLARE @IdAmilpa INT = (SELECT id_ruta FROM Rutas WHERE nombre_corto = 'amilpa');

INSERT INTO Horarios_Ruta (id_ruta, turno, hora_llegada) VALUES
(@IdAmilpa, 'matutino', '07:00'), (@IdAmilpa, 'matutino', '07:30'), (@IdAmilpa, 'matutino', '08:10'), 
(@IdAmilpa, 'matutino', '08:40'), (@IdAmilpa, 'matutino', '09:10'), (@IdAmilpa, 'matutino', '09:40'), 
(@IdAmilpa, 'matutino', '10:10'), (@IdAmilpa, 'matutino', '10:40'), (@IdAmilpa, 'matutino', '11:10'), 
(@IdAmilpa, 'matutino', '11:40'), (@IdAmilpa, 'matutino', '12:10'), (@IdAmilpa, 'matutino', '12:40'), 
(@IdAmilpa, 'matutino', '13:10'), (@IdAmilpa, 'matutino', '13:40'),
(@IdAmilpa, 'vespertino', '14:10'), (@IdAmilpa, 'vespertino', '14:40'), (@IdAmilpa, 'vespertino', '15:10'), 
(@IdAmilpa, 'vespertino', '15:40'), (@IdAmilpa, 'vespertino', '16:10'), (@IdAmilpa, 'vespertino', '16:40'), 
(@IdAmilpa, 'vespertino', '17:10'), (@IdAmilpa, 'vespertino', '17:40'), (@IdAmilpa, 'vespertino', '18:10'), 
(@IdAmilpa, 'vespertino', '18:40'), (@IdAmilpa, 'vespertino', '19:10'), (@IdAmilpa, 'vespertino', '19:40'), 
(@IdAmilpa, 'vespertino', '20:10'), (@IdAmilpa, 'vespertino', '20:40'), (@IdAmilpa, 'vespertino', '21:10'), 
(@IdAmilpa, 'vespertino', '21:40');

-- Insertando datos Violeta
DECLARE @IdVioleta INT = (SELECT id_ruta FROM Rutas WHERE nombre_corto = 'violeta');

INSERT INTO Horarios_Ruta (id_ruta, turno, hora_llegada) VALUES
(@IdVioleta, 'matutino', '07:00'), (@IdVioleta, 'matutino', '07:30'), (@IdVioleta, 'matutino', '08:00'), 
(@IdVioleta, 'matutino', '08:35'), (@IdVioleta, 'matutino', '09:00'), (@IdVioleta, 'matutino', '09:30'), 
(@IdVioleta, 'matutino', '10:00'), (@IdVioleta, 'matutino', '10:30'), (@IdVioleta, 'matutino', '11:00'), 
(@IdVioleta, 'matutino', '11:30'), (@IdVioleta, 'matutino', '12:00'), (@IdVioleta, 'matutino', '12:30'), 
(@IdVioleta, 'matutino', '13:00'), (@IdVioleta, 'matutino', '13:30'),
(@IdVioleta, 'vespertino', '14:00'), (@IdVioleta, 'vespertino', '14:30'), (@IdVioleta, 'vespertino', '15:00'), 
(@IdVioleta, 'vespertino', '15:30'), (@IdVioleta, 'vespertino', '16:00'), (@IdVioleta, 'vespertino', '16:30'), 
(@IdVioleta, 'vespertino', '17:00'), (@IdVioleta, 'vespertino', '17:30'), (@IdVioleta, 'vespertino', '18:00'), 
(@IdVioleta, 'vespertino', '18:30'), (@IdVioleta, 'vespertino', '19:00'), (@IdVioleta, 'vespertino', '19:30'), 
(@IdVioleta, 'vespertino', '20:00'), (@IdVioleta, 'vespertino', '20:30'), (@IdVioleta, 'vespertino', '21:00'), 
(@IdVioleta, 'vespertino', '21:30');

--Insertar ubicaciones amilpa
INSERT INTO Coordenadas_Ruta (id_ruta, secuencia, latitud, longitud) VALUES 
(@IdAmilpa, 1, 32.6635, -115.4855), (@IdAmilpa, 2, 32.6582, -115.4740), (@IdAmilpa, 3, 32.6515, -115.4650),
(@IdAmilpa, 4, 32.6480, -115.4560), (@IdAmilpa, 5, 32.6465, -115.4520), (@IdAmilpa, 6, 32.6450, -115.4415),
(@IdAmilpa, 7, 32.6492, -115.4310), (@IdAmilpa, 8, 32.6530, -115.4220), (@IdAmilpa, 9, 32.6601, -115.4050),
(@IdAmilpa, 10, 32.6610, -115.3930), (@IdAmilpa, 11, 32.6618, -115.3755), (@IdAmilpa, 12, 32.6510, -115.3755),
(@IdAmilpa, 13, 32.6410, -115.3755), (@IdAmilpa, 14, 32.6320, -115.3760), (@IdAmilpa, 15, 32.6285, -115.3765),
(@IdAmilpa, 16, 32.6258, -115.3770);

--Insertar ubicaciones Violeta
INSERT INTO Coordenadas_Ruta (id_ruta, secuencia, latitud, longitud) VALUES 
(@IdVioleta, 1, 32.6250, -115.4850), (@IdVioleta, 2, 32.6251, -115.4790), (@IdVioleta, 3, 32.6252, -115.4740),
(@IdVioleta, 4, 32.6258, -115.4670), (@IdVioleta, 5, 32.6265, -115.4600), (@IdVioleta, 6, 32.6290, -115.4510),
(@IdVioleta, 7, 32.6315, -115.4420), (@IdVioleta, 8, 32.6380, -115.4350), (@IdVioleta, 9, 32.6450, -115.4285),
(@IdVioleta, 10, 32.6530, -115.4295), (@IdVioleta, 11, 32.6615, -115.4310), (@IdVioleta, 12, 32.6575, -115.4250),
(@IdVioleta, 13, 32.6535, -115.4190), (@IdVioleta, 14, 32.6570, -115.4040), (@IdVioleta, 15, 32.6610, -115.3890),
(@IdVioleta, 16, 32.6618, -115.3755), (@IdVioleta, 17, 32.6540, -115.3755), (@IdVioleta, 18, 32.6465, -115.3755),
(@IdVioleta, 19, 32.6375, -115.3755), (@IdVioleta, 20, 32.6320, -115.3760), (@IdVioleta, 21, 32.6258, -115.3770);
GO