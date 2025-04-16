-- CURSOS (ID AUTOINCREMENT, asumimos que estos serán ID 1 y 2)
INSERT INTO cursos (codigo, nombre) VALUES 
('ICC5130', 'Diseno de Software Verificable'),
('ICC3102', 'Bases de Datos');

-- PROFESORES
INSERT INTO profesores (nombre, correo) VALUES 
('Maria Perez', 'mperez@uandes.cl'),
('Juan Soto', 'jsoto@uandes.cl');

-- ALUMNOS
INSERT INTO alumnos (nombre, correo, fecha_ingreso) VALUES 
('Lucia Gomez', 'lgomez@uc.cl', '2022-03-01'),
('Pedro Ruiz', 'pruiz@uc.cl', '2023-03-01');

-- INSTANCIAS (curso_id: 1 y 2)
INSERT INTO instancias (curso_id, anio, semestre) VALUES 
(1, 2025, 1),
(2, 2025, 2);

-- SECCIONES (instancia_id: 1 y 2)
INSERT INTO secciones (instancia_id, numero) VALUES 
(1, 1),
(2, 1);

-- ASIGNACIONES DE PROFESORES
INSERT INTO asignaciones_profesores (seccion_id, profesor_id) VALUES 
(1, 1),
(2, 2);

-- INSCRIPCIONES
INSERT INTO inscripciones (seccion_id, alumno_id) VALUES 
(1, 1),
(2, 2);

-- EVALUACIONES (seccion_id: 1)
INSERT INTO evaluaciones (seccion_id, tipo, peso, es_opcional) VALUES 
(1, 'Tarea', 40, FALSE),
(1, 'Control', 60, TRUE);

-- NOTAS (evaluacion_id: 1 y 2, alumno_id: 1)
INSERT INTO notas (evaluacion_id, alumno_id, nota) VALUES 
(1, 1, 6.5),
(2, 1, 5.0);
