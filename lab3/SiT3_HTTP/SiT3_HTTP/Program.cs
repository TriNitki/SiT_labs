namespace SiT3_HTTP;

internal class Program
{
    static async Task Main(string[] args)
    {
        var url = "https://a.d-cd.net";
        var imageRelativePath = "/xoAAAgNdkOA-1920.jpg";
        var outputFilePath = $"{AppDomain.CurrentDomain.BaseDirectory}downloaded_image.jpg";

        using (var client = new HttpClient())
        {
            client.BaseAddress = new Uri(url);

            var response = await client.GetAsync(imageRelativePath);

            Console.WriteLine("Response Headers:");
            foreach (var header in response.Headers)
                Console.WriteLine($"{header.Key}: {string.Join(", ", header.Value)}");
            

            if (response.IsSuccessStatusCode)
            {
                await DownloadImageAsync(client, imageRelativePath, outputFilePath);
                Console.WriteLine($"Image downloaded successfully to {outputFilePath}");
            }
            else
            {
                Console.WriteLine($"Failed to access the URL. Status Code: {response.StatusCode}");
            }
        }
    }

    static async Task DownloadImageAsync(HttpClient client, string imageUrl, string filePath)
    {
        HttpResponseMessage imageResponse = await client.GetAsync(imageUrl);

        if (imageResponse.IsSuccessStatusCode)
        {
            byte[] imageBytes = await imageResponse.Content.ReadAsByteArrayAsync();
            await File.WriteAllBytesAsync(filePath, imageBytes);
        }
        else
        {
            Console.WriteLine($"Failed to download the image. Status Code: {imageResponse.StatusCode}");
        }
    }
}