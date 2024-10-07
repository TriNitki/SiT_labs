using System.Net.Security;
using System.Net.Sockets;
using System.Text;

namespace SiT2_receiver;

class Program
{
    static void Main(string[] args)
    {
        // Your Gmail credentials
        var username = "fsb2004pro@gmail.com";
        var password = "hcmb wthg qkpf qtyj";

        // Connect to the Gmail IMAP server (IMAP over SSL port: 993)
        using var client = new TcpClient("imap.gmail.com", 993);
        using (var sslStream = new SslStream(client.GetStream()))
        {
            sslStream.AuthenticateAsClient("imap.gmail.com");

            using (var reader = new StreamReader(sslStream, Encoding.ASCII))
            using (var writer = new StreamWriter(sslStream, Encoding.ASCII))
            {
                writer.AutoFlush = true;
                Console.WriteLine("Connected to Gmail IMAP server over SSL...");

                Console.WriteLine(ReadResponse(reader, "*"));

                SendCommand(writer, reader, $"a1 LOGIN \"{username}\" \"{password}\"\r\n");

                SendCommand(writer, reader, "a2 SELECT INBOX\r\n");

                var id = GetIdCommand(writer, reader);
                SendCommand(writer, reader, $"a4 FETCH {id} (BODY[TEXT] BODY[HEADER.FIELDS (FROM TO SUBJECT DATE)])\r\n");

                SendCommand(writer, reader, "a5 LOGOUT\r\n");
            }
        }
    }



    static string ReadResponse(StreamReader reader, string commandTag)
    {
        StringBuilder response = new StringBuilder();

        while (reader.ReadLine() is { } line)
        {
            response.AppendLine(line);
            if (line.StartsWith(commandTag) && (line.Contains("OK") || line.Contains("NO") || line.Contains("BAD")))
                break;
        }
        return response.ToString();
    }

    static string GetIdCommand(StreamWriter writer, StreamReader reader)
    {
        var command = "a3 SEARCH ALL\r\n";
        var commandTag = command.Split(' ')[0];

        Console.WriteLine($"Sending: {command}");
        writer.Write(command);
        var id = ReadResponse(reader, commandTag).Split(' ')[^5];
        var response = id[..id.IndexOf("\r", StringComparison.Ordinal)];
        Console.WriteLine($"Id: {response}");
        return response;
    }

    static void SendCommand(StreamWriter writer, StreamReader reader, string command)
    {
        var commandTag = command.Split(' ')[0];

        Console.WriteLine($"Sending: {command}");
        writer.Write(command);
        var response = ReadResponse(reader, commandTag);
        Console.WriteLine($"Response: {response}");
    }
}