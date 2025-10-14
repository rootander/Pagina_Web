package Backend.dto;

import lombok.RequiredArgsConstructor;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.method.configuration.EnableMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;
import org.springframework.web.client.RestTemplate;

@Configuration
@EnableMethodSecurity
@RequiredArgsConstructor
public class SecurityConfig {

    @Bean
    RestTemplate restTemplate() {
        return new RestTemplate();
    }

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http, JwtAuthFilter jwtFilter) throws Exception {
        http
            .csrf(csrf -> csrf.disable())
            .sessionManagement(s -> s.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .authorizeHttpRequests(auth -> auth

                // Recursos públicos: estáticos, login, página principal
                .requestMatchers(
                    "/", "/index", "/pages/index",
                    "/css/**", "/js/**", "/images/**",
                    "/auth/**", "/esperando-login"
                ).permitAll()

                // Páginas accesibles sin login (ajústalo si necesitas protección)
                .requestMatchers(
                    "/dashboard",
                    "/productos",
                    "/inventario",    // <-- déjalo aquí solo si quieres acceso libre
                    "/categorias",
                    "/usuarios",
                    "/proveedores",
                    "/empleados",
                    "/empleados/**",
                    "/movimientos"
                ).permitAll()

                // APIs públicas (si aplica)
                .requestMatchers(
                    "/api/usuarios/**",
                    "/api/categorias/**",
                    "/api/proveedores/**",
                    "/api/productos/**",
                    "/api/tallas/**",
                    "/api/producto-talla/**",
                    "/api/empleados/**",
                    "/api/movimientos/**"
                ).permitAll()

                // Si quieres restringir rutas específicas por rol:
                //.requestMatchers("/inventario").hasRole("ADMIN")  // <--- Úsalo si quieres protegerla

                .anyRequest().authenticated()
            )
            .addFilterBefore(jwtFilter, UsernamePasswordAuthenticationFilter.class);

        return http.build();
    }
}

