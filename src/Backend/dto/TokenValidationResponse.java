package Backend.dto;

import lombok.Data;

@Data
public class TokenValidationResponse { private boolean valid; private String username; }
