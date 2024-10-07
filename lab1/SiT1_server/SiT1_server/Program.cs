var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();

var app = builder.Build();

app.MapControllers();

app.MapGet("/", () => DateTimeOffset.Now.ToUnixTimeSeconds());

app.Run();
