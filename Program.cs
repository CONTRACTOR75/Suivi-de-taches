using Microsoft.EntityFrameworkCore;
using SuiviDeTaches;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.

builder.Services.AddControllers();
builder.Services.AddDbContext<TaskDbContext>(options =>
    options.UseMySql(
        "server=localhost;port=3308;database=nom_de_ta_base;user=ton_utilisateur;password=ton_mot_de_passe",
        new MySqlServerVersion(new Version(8, 0, 36)) // Mets ici la version de ton serveur MySQL
    )
);
// Learn more about configuring OpenAPI at https://aka.ms/aspnet/openapi
builder.Services.AddOpenApi();

var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.MapOpenApi();
}

app.UseHttpsRedirection();

app.UseAuthorization();

app.MapControllers();

app.Run();
