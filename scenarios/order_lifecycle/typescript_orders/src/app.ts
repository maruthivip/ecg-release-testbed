import express from "express";
import { orderRouter } from "./order-routes";

export const app = express();
app.use(express.json());
app.use("/api/v1", orderRouter);
