package example;

import jakarta.ejb.Local;

@Local
public interface Pricing {
    int total(int amount);
}
