using System.Threading.Tasks;
using Azure.Messaging.ServiceBus;
using Azure.Messaging.EventHubs.Producer;

namespace ReleaseFixtures;

public class Orders
{
    public async Task SendQueue(ServiceBusClient client)
    {
        ServiceBusSender sender = client.CreateSender("release-orders");
        await sender.SendMessageAsync(new ServiceBusMessage("order"));
    }

    public async Task SendEvent(EventHubProducerClient producer)
    {
        using EventDataBatch batch = await producer.CreateBatchAsync();
        if (!batch.TryAdd(new Azure.Messaging.EventHubs.EventData(System.Text.Encoding.UTF8.GetBytes("order"))))
            throw new System.InvalidOperationException("Event did not fit");
        await producer.SendAsync(batch);
    }
}
