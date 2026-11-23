import { Router } from "express";
import { findOrder, insertOrder } from "./order-repository";

export const orderRouter = Router();

orderRouter.post("/orders", async (req, res, next) => {
  try {
    const { orderId, customerId, totalCents } = req.body;
    if (!orderId || !customerId || !Number.isInteger(totalCents) || totalCents <= 0) {
      res.status(400).json({ error: "invalid order" });
      return;
    }
    await insertOrder({ orderId, customerId, totalCents, status: "PENDING" });
    res.status(201).json({ orderId });
  } catch (error) {
    next(error);
  }
});

orderRouter.get("/orders/:orderId", async (req, res, next) => {
  try {
    const order = await findOrder(req.params.orderId);
    if (!order) {
      res.sendStatus(404);
      return;
    }
    res.json(order);
  } catch (error) {
    next(error);
  }
});
