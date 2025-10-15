package com.inventario.sistema.controllers;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.inventario.sistema.entities.Empleado;
import com.inventario.sistema.entities.Usuario;
import com.inventario.sistema.services.EmpleadoService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.io.BufferedReader;
import java.io.File;
import java.io.InputStreamReader;
import java.math.BigDecimal;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/empleados")
@RequiredArgsConstructor
public class EmpleadoController {

    private final EmpleadoService empleadoService;

    @PostMapping
    public ResponseEntity<?> crearEmpleadoConUsuario(@RequestBody Map<String, Object> datos) {
        try {
            Map<String, Object> usuarioMap = (Map<String, Object>) datos.get("usuario");
Usuario usuario = new Usuario();
usuario.setUsername((String) usuarioMap.get("username"));
usuario.setEmail((String) usuarioMap.get("email"));

String rol = (String) usuarioMap.get("rol");
if (rol == null || rol.isBlank()) {
    return ResponseEntity.badRequest().body(Map.of("error", "El campo 'rol' es obligatorio"));
}
usuario.setRol(rol.toUpperCase());

usuario.setFaceEncoding((String) usuarioMap.get("faceEncoding"));


            Empleado empleado = new Empleado();
            empleado.setUsuario(usuario);
            empleado.setNombre((String) datos.get("nombre"));
            empleado.setApellido((String) datos.get("apellido"));
            empleado.setDni((String) datos.get("dni"));
            empleado.setTelefono((String) datos.get("telefono"));
            empleado.setDireccion((String) datos.get("direccion"));

            Object salarioObj = datos.get("salario");
            BigDecimal salario = BigDecimal.ZERO;
            if (salarioObj != null && !salarioObj.toString().isBlank()) {
                try {
                    salario = new BigDecimal(salarioObj.toString());
                } catch (NumberFormatException ignored) {
                    salario = BigDecimal.ZERO;
                }
            }
            empleado.setSalario(salario);

            Empleado saved = empleadoService.crearEmpleado(empleado);
            return ResponseEntity.status(201).body(saved);

        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }


@GetMapping("/capturar-rostro")
public ResponseEntity<?> capturarRostro() {
    try {
        
        String pythonCmd = "python";
        String scriptPath = "C:\\Users\\usuario\\Pictures\\Sistema_inventario_biometrico\\sistema\\python\\face_capture.py";

        ProcessBuilder pb = new ProcessBuilder("cmd.exe", "/c", "start", "", pythonCmd, scriptPath);
        pb.directory(new File("C:\\Users\\usuario\\Pictures\\Sistema_inventario_biometrico\\sistema"));
        pb.redirectErrorStream(true);
        pb.start();

        return ResponseEntity.ok(Map.of("mensaje", "✔ Cámara abierta. Presiona ESPACIO para capturar el rostro."));
    } catch (Exception e) {
        return ResponseEntity.status(500).body(Map.of(
                "error", "No se pudo iniciar el proceso de captura",
                "detalle", e.toString()
        ));
    }
}






    @GetMapping("/obtener-encoding")
    public ResponseEntity<?> obtenerEncoding() {
        File jsonFile = new File("C:\\Users\\usuario\\Pictures\\Sistema_inventario_biometrico\\sistema\\python\\encoding.json");

        if (!jsonFile.exists()) {
            return ResponseEntity.status(404).body(Map.of("error", "encoding.json no encontrado"));
        }

        try {
            ObjectMapper mapper = new ObjectMapper();
            Map<String, Object> encodingData = mapper.readValue(jsonFile, Map.class);
            return ResponseEntity.ok(encodingData);
        } catch (Exception e) {
            return ResponseEntity.status(500).body(Map.of("error", "Error leyendo encoding.json", "details", e.getMessage()));
        }
    }

    @GetMapping
    public ResponseEntity<List<Empleado>> listar() {
        return ResponseEntity.ok(empleadoService.listar());
    }

    @GetMapping("/{id}")
    public ResponseEntity<?> obtener(@PathVariable Integer id) {
        return empleadoService.obtener(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }
}
