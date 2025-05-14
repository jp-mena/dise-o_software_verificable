-- CURSOS
CREATE TABLE cursos (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    codigo TEXT NOT NULL,
    nombre TEXT NOT NULL
);

-- CURSOS REQUISITO DE OTROS
CREATE TABLE requisitos (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    curso_id BIGINT,
    requisito_id BIGINT,
    FOREIGN KEY (curso_id) REFERENCES cursos(id) ON DELETE CASCADE,
    FOREIGN KEY (requisito_id) REFERENCES cursos(id) ON DELETE CASCADE
);

-- INSTANCIAS DE CURSO
CREATE TABLE instancias (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    curso_id BIGINT,
    anio INT NOT NULL,
    semestre INT NOT NULL,
    FOREIGN KEY (curso_id) REFERENCES cursos(id) ON DELETE CASCADE
);

-- SECCIONES
CREATE TABLE secciones (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    instancia_id BIGINT,
    numero INT NOT NULL,
    modo_evaluacion ENUM('peso', 'porcentaje') DEFAULT 'porcentaje',
    FOREIGN KEY (instancia_id) REFERENCES instancias(id) ON DELETE CASCADE
);

-- PROFESORES
CREATE TABLE profesores (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    nombre TEXT NOT NULL,
    correo TEXT NOT NULL
);

-- ALUMNOS
CREATE TABLE alumnos (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    nombre TEXT NOT NULL,
    correo TEXT NOT NULL,
    fecha_ingreso DATE NOT NULL
);

-- TÓPICOS GENERALES
CREATE TABLE topicos (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    nombre TEXT NOT NULL
);

-- TÓPICOS ASIGNADOS A SECCIÓN
CREATE TABLE topicos_por_seccion (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    topico_id BIGINT,
    seccion_id BIGINT,
    porcentaje_total DECIMAL(5,2) NOT NULL CHECK (porcentaje_total >= 0.0 AND porcentaje_total <= 100.0),
    FOREIGN KEY (topico_id) REFERENCES topicos(id) ON DELETE CASCADE,
    FOREIGN KEY (seccion_id) REFERENCES secciones(id) ON DELETE CASCADE
);

-- EVALUACIONES DENTRO DE UN TÓPICO POR SECCIÓN
CREATE TABLE evaluaciones (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    topico_seccion_id BIGINT,
    orden INT,
    valor DECIMAL(5,2) NOT NULL CHECK (valor >= 0.0),
    tipo ENUM('peso', 'porcentaje') NOT NULL,
    obligatoria BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (topico_seccion_id) REFERENCES topicos_por_seccion(id) ON DELETE CASCADE
);

-- NOTAS DE EVALUACIONES
CREATE TABLE notas (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    evaluacion_id BIGINT,
    alumno_id BIGINT,
    nota DECIMAL(3,1) NOT NULL CHECK (nota >= 0.0 AND nota <= 7.0),
    FOREIGN KEY (evaluacion_id) REFERENCES evaluaciones(id) ON DELETE CASCADE,
    FOREIGN KEY (alumno_id) REFERENCES alumnos(id) ON DELETE CASCADE
);

-- ASIGNACIONES DE PROFESORES A SECCIÓN
CREATE TABLE asignaciones_profesores (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    seccion_id BIGINT,
    profesor_id BIGINT,
    FOREIGN KEY (seccion_id) REFERENCES secciones(id) ON DELETE CASCADE,
    FOREIGN KEY (profesor_id) REFERENCES profesores(id) ON DELETE CASCADE
);

-- INSCRIPCIONES DE ALUMNOS A SECCIÓN
CREATE TABLE inscripciones (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    seccion_id BIGINT,
    alumno_id BIGINT,
    FOREIGN KEY (seccion_id) REFERENCES secciones(id) ON DELETE CASCADE,
    FOREIGN KEY (alumno_id) REFERENCES alumnos(id) ON DELETE CASCADE
);
