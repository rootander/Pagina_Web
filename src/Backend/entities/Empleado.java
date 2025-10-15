package com.inventario.sistema.entities;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonInclude;
import jakarta.persistence.*;
import jakarta.validation.constraints.*;
import lombok.*;

import java.math.BigDecimal;

@Entity
@Data
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
@Table(name = "empleados")
public class Empleado {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "emp_id")
    private Integer id;

    @OneToOne(optional = false, cascade = CascadeType.ALL, fetch = FetchType.EAGER)
    @JoinColumn(name = "usuario_id", referencedColumnName = "usuario_id", nullable = false, unique = true)
    @JsonIgnoreProperties("empleado") 
    private Usuario usuario;

    @NotBlank
    @Size(max = 100)
    @Column(name = "emp_nombre", nullable = false)
    private String nombre;

    @NotBlank
    @Size(max = 100)
    @Column(name = "emp_apellido", nullable = false)
    private String apellido;

    @NotBlank
    @Size(max = 20)
    @Column(name = "emp_dni", nullable = false, unique = true)
    private String dni;

    @Size(max = 255)
    private String direccion;

    @Size(max = 20)
    private String telefono;

    @DecimalMin(value = "0.0", inclusive = true)
    @Digits(integer = 10, fraction = 2)
    @Column(precision = 10, scale = 2)
    private BigDecimal salario;
}
