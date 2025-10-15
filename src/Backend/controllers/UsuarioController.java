package com.inventario.sistema.controllers;

import com.inventario.sistema.entities.Usuario;
import com.inventario.sistema.repositories.UsuarioRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/usuarios")
@RequiredArgsConstructor
public class UsuarioController {

    private final UsuarioRepository usuarioRepository;

    @PostMapping
    public ResponseEntity<?> crearUsuario(@RequestBody Usuario usuario) {
        if (usuarioRepository.findByUsername(usuario.getUsername()).isPresent()) {
            return ResponseEntity.badRequest()
                    .body("El usuario ya existe: " + usuario.getUsername());
        }

        try {
            Usuario saved = usuarioRepository.save(usuario);
            return ResponseEntity.status(201).body(saved);
        } catch (Exception e) {
            return ResponseEntity.status(500)
                    .body("Error al guardar usuario: " + e.getMessage());
        }
    }

    @GetMapping("/{username}")
    public ResponseEntity<Usuario> obtenerPorUsername(@PathVariable String username) {
        return usuarioRepository.findByUsername(username)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    
    @GetMapping
    public ResponseEntity<List<Usuario>> listarUsuarios() {
        return ResponseEntity.ok(usuarioRepository.findAll());
    }
}
