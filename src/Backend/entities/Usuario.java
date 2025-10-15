package com.inventario.sistema.entities;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonInclude;
import jakarta.persistence.*;
import jakarta.validation.constraints.*;
import lombok.*;

@Entity
@Data
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
@Table(name = "usuarios")
public class Usuario {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "usuario_id")
    private Integer id;

    @Column(name = "ext_id")
    private String externalId;

    @NotBlank
    @Size(max = 100)
    @Column(name = "usr_user", unique = true, nullable = false)
    private String username;

    @Email
    @Size(max = 150)
    @Column(name = "usr_email", unique = true)
    private String email;

    @Lob
    @Column(name = "usr_face_encoding", columnDefinition = "LONGTEXT")
    private String faceEncoding;

    @NotBlank
    @Size(max = 50)
    @Column(name = "usr_rol", nullable = false)
    private String rol;

    @Column(name = "usr_act", nullable = false)
    private Boolean activo = true;

    @OneToOne(mappedBy = "usuario", cascade = CascadeType.ALL)
    @JsonIgnoreProperties("usuario") 
    private Empleado empleado;
}
