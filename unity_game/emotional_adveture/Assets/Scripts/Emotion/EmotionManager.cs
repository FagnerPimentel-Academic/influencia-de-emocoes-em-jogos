using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using UnityEngine;

public class EmotionManager : MonoBehaviour
{
    private TcpListener server;
    private bool isRunning = false;

    void Start()
    {
        StartServer();
    }

    void StartServer()
    {
        try
        {
            server = new TcpListener(IPAddress.Parse("127.0.0.1"), 65432);
            server.Start();
            isRunning = true;
            Debug.Log("Servidor Unity rodando e aguardando conexões...");

            // Inicia a escuta em uma thread separada para não travar o jogo
            server.BeginAcceptTcpClient(AcceptClient, server);
        }
        catch (Exception e)
        {
            Debug.LogError($"Erro ao iniciar o servidor: {e.Message}");
        }
    }

    void AcceptClient(IAsyncResult ar)
    {
        if (!isRunning) return;

        TcpListener listener = (TcpListener)ar.AsyncState;
        TcpClient client = listener.EndAcceptTcpClient(ar);
        NetworkStream stream = client.GetStream();

        byte[] buffer = new byte[1024];
        int bytesRead = stream.Read(buffer, 0, buffer.Length);
        string jsonData = Encoding.UTF8.GetString(buffer, 0, bytesRead);

        Debug.Log($"Dados recebidos do Python: {jsonData}");

        // Analisa os dados JSON
        ProcessJsonData(jsonData);

        // Fecha a conexão com o cliente
        client.Close();

        // Continua escutando por novos clientes
        server.BeginAcceptTcpClient(AcceptClient, server);
    }

    void ProcessJsonData(string jsonData)
    {
        // Aqui você pode analisar o JSON recebido e usar as informações conforme necessário
        // Exemplo de como você pode trabalhar com o JSON em Unity
        EmotionData emotions = JsonUtility.FromJson<EmotionData>(jsonData);
        Debug.Log($"Happy: {emotions.Happy}, Sad: {emotions.Sad}, Angry: {emotions.Angry}, Scary: {emotions.Scary}");
    }

    void OnApplicationQuit()
    {
        isRunning = false;
        server.Stop();
    }

    // Classe para mapear os dados JSON
    [Serializable]
    public class EmotionData
    {
        public int Happy;
        public int Sad;
        public int Angry;
        public int Scary;
    }
}
