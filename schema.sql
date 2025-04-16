CREATE TABLE cursos (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    codigo TEXT NOT NULL,
    nombre TEXT NOT NULL
);

CREATE TABLE requisitos (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    curso_id BIGINT,
    requisito_id BIGINT,
    FOREIGN KEY (curso_id) REFERENCES cursos(id) ON DELETE CASCADE,
    FOREIGN KEY (requisito_id) REFERENCES cursos(id) ON DELETE CASCADE
);

CREATE TABLE instancias (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    curso_id BIGINT,
    anio INT NOT NULL,
    semestre INT NOT NULL,
    FOREIGN KEY (curso_id) REFERENCES cursos(id) ON DELETE CASCADE
);

CREATE TABLE secciones (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    instancia_id BIGINT,
    numero INT NOT NULL,
    FOREIGN KEY (instancia_id) REFERENCES instancias(id) ON DELETE CASCADE
);

CREATE TABLE profesores (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    nombre TEXT NOT NULL,
    correo TEXT NOT NULL
);

CREATE TABLE alumnos (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    nombre TEXT NOT NULL,
    correo TEXT NOT NULL,
    fecha_ingreso DATE NOT NULL
);

CREATE TABLE evaluaciones (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    seccion_id BIGINT,
    tipo TEXT NOT NULL,
    peso DECIMAL(5,2) NOT NULL,
    es_opcional BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (seccion_id) REFERENCES secciones(id) ON DELETE CASCADE
);

CREATE TABLE notas (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    evaluacion_id BIGINT,
    alumno_id BIGINT,
    nota DECIMAL(3,1) NOT NULL,
    FOREIGN KEY (evaluacion_id) REFERENCES evaluaciones(id) ON DELETE CASCADE,
    FOREIGN KEY (alumno_id) REFERENCES alumnos(id) ON DELETE CASCADE
);

CREATE TABLE asignaciones_profesores (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    seccion_id BIGINT,
    profesor_id BIGINT,
    FOREIGN KEY (seccion_id) REFERENCES secciones(id) ON DELETE CASCADE,
    FOREIGN KEY (profesor_id) REFERENCES profesores(id) ON DELETE CASCADE
);

CREATE TABLE inscripciones (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    seccion_id BIGINT,
    alumno_id BIGINT,
    FOREIGN KEY (seccion_id) REFERENCES secciones(id) ON DELETE CASCADE,
    FOREIGN KEY (alumno_id) REFERENCES alumnos(id) ON DELETE CASCADE
);
