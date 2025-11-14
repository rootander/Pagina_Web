# Tabla: empleados

```sql
CREATE TABLE empleados (
    emp_id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL UNIQUE,
    emp_nombre VARCHAR(100) NOT NULL,
    emp_apellido VARCHAR(100) NOT NULL,
    emp_dni VARCHAR(20) NOT NULL UNIQUE,
    direccion VARCHAR(255),
    telefono VARCHAR(20),
    salario DECIMAL(10,2) DEFAULT 0.00,

    CONSTRAINT fk_empleado_usuario
        FOREIGN KEY (usuario_id)
        REFERENCES usuarios(usuario_id)
);
```
