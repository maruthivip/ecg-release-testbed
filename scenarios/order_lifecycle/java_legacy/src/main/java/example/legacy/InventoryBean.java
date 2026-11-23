package example.legacy;

import jakarta.ejb.Stateless;

@Stateless
public class InventoryBean implements InventoryGateway {
    @Override
    public boolean reserve(String orderId) {
        return orderId != null && !orderId.isBlank();
    }
}
