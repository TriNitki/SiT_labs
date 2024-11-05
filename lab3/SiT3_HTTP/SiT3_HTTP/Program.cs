using System.Net.Security;
using System.Net.Sockets;
using System.Text;

namespace SiT3_HTTP;

internal class Program
{
    private const string Host = "a.d-cd.net";
    private const int Port = 443;

    internal static async Task Main(string[] args)
    {
        const string imageRelativePath = "/xoAAAgNdkOA-1920.jpg";
        var outputFilePath = $"{AppDomain.CurrentDomain.BaseDirectory}downloaded_image.jpg";

        try
        {
            using var client = new TcpClient(Host, Port);
            await using var sslStream = new SslStream(client.GetStream(), false);

            await sslStream.AuthenticateAsClientAsync(Host);

            const string request = $"GET {imageRelativePath} HTTP/1.1\r\n" +
                                   $"Host: {Host}\r\n" +
                                   "Connection: close\r\n\r\n";

            var requestBytes = Encoding.ASCII.GetBytes(request);
            await sslStream.WriteAsync(requestBytes, 0, requestBytes.Length);
            await sslStream.FlushAsync();

            using var memoryStream = new MemoryStream();
            var buffer = new byte[4096];
            int bytesRead;

            while ((bytesRead = await sslStream.ReadAsync(buffer, 0, buffer.Length)) > 0)
            {
                memoryStream.Write(buffer, 0, bytesRead);
            }

            var response = Encoding.ASCII.GetString(memoryStream.ToArray());
            var headerEndIndex = response.IndexOf("\r\n\r\n", StringComparison.Ordinal);

            if (headerEndIndex == -1)
            {
                Console.WriteLine("Некорректный ответ от сервера.");
                return;
            }

            var headers = response[..headerEndIndex];
            var imageData = memoryStream.ToArray()[(headerEndIndex + 4)..];

            Console.WriteLine("Response Headers:");
            Console.WriteLine(headers);

            if (headers.Contains("200 OK"))
            {
                await File.WriteAllBytesAsync(outputFilePath, imageData);
                Console.WriteLine($"Image downloaded successfully to {outputFilePath}");
            }
            else
            {
                Console.WriteLine("Failed to access the URL. Response headers:");
                Console.WriteLine(headers);
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"An error occurred: {ex.Message}");
        }
    }
}