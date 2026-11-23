package example.legacy;

import jakarta.ejb.EJB;
import jakarta.enterprise.context.RequestScoped;
import jakarta.inject.Named;

@Named("orderView")
@RequestScoped
public class OrderView {
    @EJB
    private OrderWorkflow workflow;
    private String orderId;
    private int amount;
    private String result;

    public String getOrderId() { return orderId; }
    public void setOrderId(String orderId) { this.orderId = orderId; }
    public int getAmount() { return amount; }
    public void setAmount(int amount) { this.amount = amount; }
    public String getResult() { return result; }

    public String submit() {
        result = workflow.submit(orderId, amount);
        return "summary?faces-redirect=true";
    }
}
