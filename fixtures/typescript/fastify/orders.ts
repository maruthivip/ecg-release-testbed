import Fastify from "fastify";

const app = Fastify();
app.get<{ Params: { id: string } }>("/release/orders/:id", async (request) => {
  return request.params.id;
});
