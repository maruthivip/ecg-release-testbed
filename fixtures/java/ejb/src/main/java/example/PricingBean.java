package example;

import jakarta.ejb.Stateless;

@Stateless
public class PricingBean implements Pricing {
    public int total(int amount) {
        return amount + 5;
    }
}
