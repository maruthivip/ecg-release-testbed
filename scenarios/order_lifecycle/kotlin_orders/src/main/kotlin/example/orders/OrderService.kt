package example.orders

class OrderService {
    fun create(order: CreateOrder): String {
        require(order.totalCents > 0)
        return order.orderId
    }

    fun get(orderId: String): String = orderId
}
