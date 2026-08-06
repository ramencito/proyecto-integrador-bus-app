USE UPBC_Bus_DB;
GO
--Tabla registros de acceso
CREATE TABLE Alumnos_Registro (
    id_registro INT IDENTITY(1,1) PRIMARY KEY,matricula VARCHAR(20) NOT NULL,nombre_alumno VARCHAR(100) NOT NULL,fecha_acceso DATETIME DEFAULT GETDATE());
GO

select * from Alumnos_Registro;