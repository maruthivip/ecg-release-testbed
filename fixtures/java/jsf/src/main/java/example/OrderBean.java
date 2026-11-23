package example;

import jakarta.enterprise.context.RequestScoped;
import jakarta.inject.Named;

@Named("orderBean")
@RequestScoped
public class OrderBean {
    private String item;

    public String getItem() {
        return item;
    }

    public void setItem(String item) {
        this.item = item;
    }

    public String submit() {
        return "confirmation";
    }
}
