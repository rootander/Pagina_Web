package Backend.dto;

import lombok.Data;
import java.util.List;

@Data
public class LoginRequest {
    private String username;
    private List<Double> faceEncoding; 
}
