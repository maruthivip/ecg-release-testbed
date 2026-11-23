package example.legacy;

import jakarta.ejb.EJB;
import jakarta.ejb.Stateless;
import jakarta.ejb.TransactionAttribute;
import jakarta.ejb.TransactionAttributeType;

@Stateless
@TransactionAttribute(TransactionAttributeType.REQUIRED)
public class OrderWorkflowBean implements OrderWorkflow {
    @EJB
    private InventoryGateway inventory;

    @Override
    public String submit(String orderId, int amount) {
        if (amount <= 0 || !inventory.reserve(orderId)) {
            return "rejected";
        }
        return "accepted";
    }
}
