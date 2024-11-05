using System.Net.NetworkInformation;

namespace SiT4_Sender;

internal class Program
{
    internal static async Task Main(string[] args)
    {
        const string targetIp = "127.0.0.1";

        await SendIcmpPacket(targetIp);
    }

    private static async Task SendIcmpPacket(string ipAddress)
    {
        using var pingSender = new Ping();
        var reply = await pingSender.SendPingAsync(ipAddress, 1000);
        Console.WriteLine(reply.Status == IPStatus.Success
            ? $"ICMP packet sent to {ipAddress}"
            : $"ICMP packet not sent: {reply.Status}");
    }
}