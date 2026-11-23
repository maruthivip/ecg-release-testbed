package example.legacy;

import jakarta.ejb.Local;

@Local
public interface OrderWorkflow {
    String submit(String orderId, int amount);
}
