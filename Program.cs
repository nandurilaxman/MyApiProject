var builder = WebApplication.CreateBuilder(args);
var env = builder.Environment.EnvironmentName;

builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(c =>
{
    c.SwaggerDoc("v1", new OpenApiInfo { Title = "My API", Version = "v1" });
    c.SerializeAsV2 = true; // generates YAML
});
dotnet add package Swashbuckle.AspNetCore

builder.Services.AddControllers();
var app = builder.Build();
dotnet add package Swashbuckle.AspNetCore

app.UseSwagger();
app.UseSwaggerUI();

app.MapControllers();

app.Run();
