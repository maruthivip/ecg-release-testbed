import mongoose, { Schema } from "mongoose";

const orderSchema = new Schema({ total: Number });
export const Order = mongoose.model("ReleaseOrder", orderSchema, "release_orders");

export async function saveOrder(total: number) {
  return Order.create({ total });
}

export async function findOrder(id: string) {
  return Order.findById(id).exec();
}
