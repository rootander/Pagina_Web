package com.inventario.sistema.services;

import com.inventario.sistema.entities.Empleado;
import com.inventario.sistema.entities.Usuario;
import com.inventario.sistema.repositories.EmpleadoRepository;
import com.inventario.sistema.repositories.UsuarioRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
@RequiredArgsConstructor
public class EmpleadoService {

    private final EmpleadoRepository empleadoRepo;
    private final UsuarioRepository usuarioRepo;

    public Empleado crearEmpleado(Empleado empleado) throws Exception {
        Usuario usuario = empleado.getUsuario();

        if (usuarioRepo.findByUsername(usuario.getUsername()).isPresent()) {
            throw new Exception("El usuario ya existe: " + usuario.getUsername());
        }

        // Se guarda en cascada (Empleado → Usuario)
        return empleadoRepo.save(empleado);
    }

    public List<Empleado> listar() {
        return empleadoRepo.findAll();
    }

    public Optional<Empleado> obtener(Integer id) {
        return empleadoRepo.findById(id);
    }
public long contar() {
    return empleadoRepo.count();
}


}
