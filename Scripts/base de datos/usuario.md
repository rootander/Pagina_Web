# Tabla: usuarios

```sql
CREATE TABLE usuarios (
    usuario_id INT AUTO_INCREMENT PRIMARY KEY,
    ext_id VARCHAR(255),
    usr_user VARCHAR(100) NOT NULL UNIQUE,
    usr_email VARCHAR(150) UNIQUE,
    usr_face_encoding LONGTEXT,
    usr_rol VARCHAR(50) NOT NULL,
    usr_act BOOLEAN NOT NULL DEFAULT TRUE
);
```
