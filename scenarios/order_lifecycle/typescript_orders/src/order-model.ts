import { Schema, model } from "mongoose";

export interface Order {
  orderId: string;
  customerId: string;
  totalCents: number;
  status: "PENDING" | "CONFIRMED";
}

const schema = new Schema<Order>({
  orderId: { type: String, required: true, unique: true },
  customerId: { type: String, required: true, index: true },
  totalCents: { type: Number, required: true, min: 1 },
  status: { type: String, enum: ["PENDING", "CONFIRMED"], required: true },
});

export const OrderModel = model<Order>("LifecycleOrder", schema, "lifecycle_orders");
