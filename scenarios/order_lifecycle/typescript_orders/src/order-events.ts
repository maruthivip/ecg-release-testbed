import { ServiceBusClient } from "@azure/service-bus";

export async function publishOrderCreated(
  client: ServiceBusClient,
  eventId: string,
  orderId: string,
  totalCents: number,
): Promise<void> {
  const sender = client.createSender("order-events");
  try {
    await sender.sendMessages({
      body: JSON.stringify({ event_id: eventId, order_id: orderId, total_cents: totalCents }),
      messageId: eventId,
      subject: "order.created",
      contentType: "application/json",
    });
  } finally {
    await sender.close();
  }
}
