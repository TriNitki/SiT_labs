using System.Net;
using System.Net.Sockets;
using System.Text;

class Program
{
    static void Main()
    {
        Console.WriteLine("Client .NET");
        string serverIP = "127.0.0.1";
        int serverPort = 5001;

        try
        {
            string message = Console.ReadLine();
            TcpClient client = new TcpClient(serverIP, serverPort);

            NetworkStream stream = client.GetStream();
            Console.Write("Enter a message: ");
            

            if (message.Length > 256)
            {
                Console.WriteLine("Message too long!");
                return;
            }

            // Send length of the string (as big-endian)
            int msgLength = IPAddress.HostToNetworkOrder(message.Length);
            byte[] lengthBytes = BitConverter.GetBytes(msgLength);
            stream.Write(lengthBytes, 0, lengthBytes.Length);

            // Send the string
            byte[] messageBytes = Encoding.ASCII.GetBytes(message);
            stream.Write(messageBytes, 0, messageBytes.Length);

            // Receive response from the server (half the string)
            byte[] buffer = new byte[128];
            int bytesRead = stream.Read(buffer, 0, buffer.Length);
            string response = Encoding.ASCII.GetString(buffer, 0, bytesRead);
            Console.WriteLine("Server response: " + response);

            client.Close();
        }
        catch (Exception ex)
        {
            Console.WriteLine("Exception: " + ex.Message);
        }

        Console.ReadLine();
    }
}