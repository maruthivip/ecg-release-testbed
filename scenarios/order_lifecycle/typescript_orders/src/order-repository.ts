import { Order, OrderModel } from "./order-model";

export async function insertOrder(order: Order): Promise<void> {
  await OrderModel.create(order);
}

export async function findOrder(orderId: string) {
  return OrderModel.findOne({ orderId }).lean().exec();
}

export async function confirmOrder(orderId: string): Promise<void> {
  await OrderModel.updateOne({ orderId, status: "PENDING" }, { $set: { status: "CONFIRMED" } });
}
