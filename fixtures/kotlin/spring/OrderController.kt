package example

import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.PathVariable
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController

@RestController
@RequestMapping("/release/orders")
class OrderController {
    @GetMapping("/{id}")
    fun findOrder(@PathVariable id: String): String = id
}
