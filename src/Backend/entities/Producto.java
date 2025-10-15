package com.inventario.sistema.entities;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import jakarta.persistence.*;
import jakarta.validation.constraints.*;
import lombok.*;

import java.math.BigDecimal;

@Entity
@Data
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "productos")
public class Producto {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @NotBlank
    @Size(max = 150)
    @Column(nullable = false)
    private String nombre;

    @Size(max = 255)
    private String descripcion;

    @NotNull
    @ManyToOne(fetch = FetchType.EAGER, optional = false)  
    @JoinColumn(name = "categoria_id", nullable = false)
    @JsonIgnoreProperties({"productos", "hibernateLazyInitializer", "handler"})
    private Categoria categoria;

    @NotNull
    @ManyToOne(fetch = FetchType.EAGER, optional = false)  
    @JoinColumn(name = "proveedor_id", nullable = false)
    @JsonIgnoreProperties({"productos", "hibernateLazyInitializer", "handler"})
    private Proveedor proveedor;

    @NotNull
    @DecimalMin("0.0")
    @Digits(integer = 10, fraction = 2)
    @Column(precision = 10, scale = 2, nullable = false)
    private BigDecimal precioCompra;

    @NotNull
    @DecimalMin("0.0")
    @Digits(integer = 10, fraction = 2)
    @Column(precision = 10, scale = 2, nullable = false)
    private BigDecimal precioVenta;

    @Size(max = 50)
    @Column(unique = true)
    private String sku;
}
