import express from "express";

const app = express();
app.get("/release/orders/:id", (req, res) => {
  res.send(req.params.id);
});
