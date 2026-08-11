USE UPBC_Bus_DB;
GO
DROP TABLE IF EXISTS Alumnos_Registro;
GO
CREATE TABLE Alumnos_Registro ( id_registro INT IDENTITY(1,1) PRIMARY KEY, correo_electronico VARCHAR(100) NOT NULL, nombre_alumno VARCHAR(100) NOT NULL,
fecha_acceso DATETIME DEFAULT GETDATE());
GO

select * from Alumnos_Registro;