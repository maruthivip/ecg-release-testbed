import { Controller, Get, Param } from "@nestjs/common";

@Controller("release/orders")
export class OrdersController {
  @Get(":id")
  getOrder(@Param("id") id: string): string {
    return id;
  }
}
