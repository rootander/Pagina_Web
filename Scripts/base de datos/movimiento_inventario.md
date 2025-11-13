# Tabla: movimientos_inventario

```sql
CREATE TABLE movimientos_inventario (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    producto_talla_id BIGINT NOT NULL,
    cantidad INT NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    descripcion VARCHAR(255),
    usuario_id INT NOT NULL,

    CONSTRAINT fk_mov_inv_producto_talla
        FOREIGN KEY (producto_talla_id)
        REFERENCES producto_talla(id),

    CONSTRAINT fk_mov_inv_usuario
        FOREIGN KEY (usuario_id)
        REFERENCES usuarios(usuario_id)
);
```
