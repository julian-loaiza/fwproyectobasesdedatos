-- ##################################################################
-- # Script de Creación de Base de Datos y Tablas                   #
-- # Basado en el Diagrama Entidad-Relación                         #
-- ##################################################################

-- Creación de la tabla 'docente'
-- Esta tabla almacena la información de los docentes.
CREATE TABLE docente (
    Codigo INT(11) NOT NULL AUTO_INCREMENT,
    Documento VARCHAR(20) NOT NULL UNIQUE,
    Nombre VARCHAR(100) NOT NULL,
    Direccion VARCHAR(255),
    Titulo VARCHAR(100),
    AnosExperiencia INT(11),
    PRIMARY KEY (Codigo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Creación de la tabla 'informatico'
-- Almacena los datos de los desarrolladores o personal informático.
CREATE TABLE informatico (
    Codigo INT(11) NOT NULL AUTO_INCREMENT,
    Nombre VARCHAR(100) NOT NULL,
    Tipo ENUM('Frontend', 'Backend', 'Fullstack', 'DevOps', 'Tester') NOT NULL, -- Valores de ejemplo
    Coste DECIMAL(10,2) NOT NULL,
    Lenguajes VARCHAR(255),
    PRIMARY KEY (Codigo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Creación de la tabla 'proyecto'
-- Contiene la información general de cada proyecto.
CREATE TABLE proyecto (
    Codigo INT(11) NOT NULL AUTO_INCREMENT,
    Nombre VARCHAR(100) NOT NULL,
    Aliado VARCHAR(100),
    Descripcion TEXT,
    Presupuesto DECIMAL(10,2),
    HorasEstimadas INT(11),
    FechaInicio DATE,
    FechaFin DATE,
    DocenteJefe INT(11),
    PRIMARY KEY (Codigo),
    FOREIGN KEY (DocenteJefe) REFERENCES docente(Codigo) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Creación de la tabla 'gasto'
-- Registra los gastos asociados a un proyecto.
CREATE TABLE gasto (
    Codigo INT(11) NOT NULL AUTO_INCREMENT,
    Descripcion TEXT,
    Fecha DATE NOT NULL,
    Importe DECIMAL(10,2) NOT NULL,
    TipoGasto VARCHAR(100),
    ProyectoCodigo INT(11) NOT NULL,
    PRIMARY KEY (Codigo),
    FOREIGN KEY (ProyectoCodigo) REFERENCES proyecto(Codigo) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Creación de la tabla 'fase'
-- Define las distintas fases que componen un proyecto.
CREATE TABLE fase (
    NumeroFase INT(11) NOT NULL AUTO_INCREMENT,
    Nombre VARCHAR(100) NOT NULL,
    FechaComienzo DATE,
    FechaFin DATE,
    Estado ENUM('Planificada', 'En Progreso', 'Completada', 'Cancelada') NOT NULL, -- Valores de ejemplo
    ProyectoCodigo INT(11) NOT NULL,
    PRIMARY KEY (NumeroFase),
    FOREIGN KEY (ProyectoCodigo) REFERENCES proyecto(Codigo) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Creación de la tabla 'recurso'
-- Almacena los recursos utilizados en cada fase de un proyecto.
CREATE TABLE recurso (
    Codigo INT(11) NOT NULL AUTO_INCREMENT,
    Nombre VARCHAR(100) NOT NULL,
    Descripcion TEXT,
    Tipo ENUM('Humano', 'Material', 'Software', 'Hardware') NOT NULL, -- Valores de ejemplo
    PeriodoUtilizado VARCHAR(100),
    FaseNumero INT(11) NOT NULL,
    PRIMARY KEY (Codigo),
    FOREIGN KEY (FaseNumero) REFERENCES fase(NumeroFase) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Creación de la tabla 'producto'
-- Define los productos o entregables generados en una fase.
CREATE TABLE producto (
    Codigo INT(11) NOT NULL AUTO_INCREMENT,
    Nombre VARCHAR(100) NOT NULL,
    Descripcion TEXT,
    Finalizado TINYINT(1) DEFAULT 0,
    FaseNumero INT(11) NOT NULL,
    Responsable INT(11),
    PRIMARY KEY (Codigo),
    FOREIGN KEY (FaseNumero) REFERENCES fase(NumeroFase) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (Responsable) REFERENCES informatico(Codigo) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ##################################################################
-- # Tablas Intermedias para Relaciones Muchos a Muchos             #
-- ##################################################################

-- Creación de la tabla 'informatico_proyecto'
-- Tabla de enlace para la relación N:M entre informáticos y proyectos.
CREATE TABLE informatico_proyecto (
    InformaticoCodigo INT(11) NOT NULL,
    ProyectoCodigo INT(11) NOT NULL,
    HorasAsignadas INT(11),
    PRIMARY KEY (InformaticoCodigo, ProyectoCodigo),
    FOREIGN KEY (InformaticoCodigo) REFERENCES informatico(Codigo) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (ProyectoCodigo) REFERENCES proyecto(Codigo) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Creación de la tabla 'informatico_fase'
-- Tabla de enlace para la relación N:M entre informáticos y fases.
CREATE TABLE informatico_fase (
    InformaticoCodigo INT(11) NOT NULL,
    FaseNumero INT(11) NOT NULL,
    PRIMARY KEY (InformaticoCodigo, FaseNumero),
    FOREIGN KEY (InformaticoCodigo) REFERENCES informatico(Codigo) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (FaseNumero) REFERENCES fase(NumeroFase) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;