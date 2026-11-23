package example;

import jakarta.ejb.Stateless;
import jakarta.ejb.EJB;

@Stateless
public class OrderService {
    @EJB
    Pricing pricing;

    public int checkout(int amount) {
        return pricing.total(amount);
    }
}
