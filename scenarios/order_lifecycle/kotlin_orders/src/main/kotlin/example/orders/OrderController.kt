package example.orders

import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.PathVariable
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestBody
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController

data class CreateOrder(val orderId: String, val totalCents: Int)

@RestController
@RequestMapping("/api/v2/orders")
class OrderController(private val service: OrderService) {
    @PostMapping
    fun create(@RequestBody order: CreateOrder): String = service.create(order)

    @GetMapping("/{orderId}")
    fun get(@PathVariable orderId: String): String = service.get(orderId)
}
