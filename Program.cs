var builder = WebApplication.CreateBuilder(args);
var env = builder.Environment.EnvironmentName;

builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(c =>
{
    c.SerializeAsV2 = true;
});

builder.Services.AddControllers();
var app = builder.Build();

app.UseSwagger();
app.UseSwaggerUI();

app.MapControllers();

app.Run();
