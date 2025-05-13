[ApiController]
[Route("[controller]")]
public class WeatherForecastController : ControllerBase
{
    [HttpGet]
    public IEnumerable<string> Get() => new[] { "Sunny", "Cloudy", "Rainy" };
}
