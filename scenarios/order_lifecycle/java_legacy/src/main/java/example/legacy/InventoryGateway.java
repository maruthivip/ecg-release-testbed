package example.legacy;

import jakarta.ejb.Local;

@Local
public interface InventoryGateway {
    boolean reserve(String orderId);
}
