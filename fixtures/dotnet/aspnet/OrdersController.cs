using Microsoft.AspNetCore.Mvc;

namespace ReleaseFixtures;

[ApiController]
[Route("release/orders")]
public class OrdersController : ControllerBase
{
    [HttpGet("{id}")]
    public string GetOrder(string id) => id;
}
