package com.inventario.sistema.controllers;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.inventario.sistema.dto.LoginRequest;
import com.inventario.sistema.dto.RegisterRequest;
import com.inventario.sistema.entities.Usuario;
import com.inventario.sistema.repositories.UsuarioRepository;
import com.inventario.sistema.config.JwtUtil;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.*;

@RestController
@RequiredArgsConstructor
@RequestMapping("/auth")
public class AuthProxyController {

    private final UsuarioRepository usuarioRepository;
    private final ObjectMapper objectMapper = new ObjectMapper();
    private final JwtUtil jwtUtil;

    @PostMapping("/login-face")
    public ResponseEntity<Map<String, Object>> login(@RequestBody LoginRequest req) {
        Optional<Usuario> usuarioOpt = usuarioRepository.findByUsername(req.getUsername());
        if (usuarioOpt.isEmpty()) {
            return ResponseEntity.status(404).body(Map.of("error", "Usuario no encontrado"));
        }

        Usuario usuario = usuarioOpt.get();

        List<Double> savedEncodingList;
        try {
            savedEncodingList = objectMapper.readValue(
                usuario.getFaceEncoding(), new TypeReference<List<Double>>() {}
            );
        } catch (Exception e) {
            return ResponseEntity.status(500).body(Map.of("error", "Error al parsear encoding guardado"));
        }

        List<Double> reqEncodingList = req.getFaceEncoding();
        if (reqEncodingList == null || reqEncodingList.size() != savedEncodingList.size()) {
            return ResponseEntity.badRequest().body(Map.of("error", "Face encoding inválido"));
        }

        double distance = calculateEuclideanDistance(reqEncodingList, savedEncodingList);
        if (distance > 0.6) {
            return ResponseEntity.status(401).body(Map.of("error", "Reconocimiento facial fallido"));
        }

        String rolReal = usuario.getRol().toUpperCase(); // Asegurar rol en mayúsculas
        String token = jwtUtil.generateToken(usuario.getUsername(), rolReal);

        Map<String, Object> response = new HashMap<>();
        response.put("token", token);
        response.put("username", usuario.getUsername());
        response.put("id", usuario.getId());
        response.put("rol", rolReal);

        return ResponseEntity.ok(response);
    }

    private double calculateEuclideanDistance(List<? extends Number> a, List<? extends Number> b) {
        double sum = 0;
        for (int i = 0; i < a.size(); i++) {
            double diff = a.get(i).doubleValue() - b.get(i).doubleValue();
            sum += diff * diff;
        }
        return Math.sqrt(sum);
    }

    @PostMapping("/register")
    public ResponseEntity<Map<String, Object>> register(@RequestBody RegisterRequest req) {
        Map<String, Object> result = new HashMap<>();
        result.put("message", "Usuario registrado correctamente");
        result.put("username", req.getUsername());
        return ResponseEntity.ok(result);
    }
}
