package example.legacy;

public class Decoy {
    public String submit(String orderId, int amount) {
        return "not part of the EJB or JSF flow";
    }
}
