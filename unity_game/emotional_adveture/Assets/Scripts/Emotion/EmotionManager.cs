using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using UnityEngine;

public class EmotionManager : MonoBehaviour
{
    private TcpListener server;
    private bool isRunning = false;
    private bool newData = false;

    // Classe para mapear os dados JSON
    [Serializable]
    public class EmotionData
    {
        public float Happy;
        public float Sad;
        public float Angry;
        public float Scary;
    }

    EmotionData currentEmotions;

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
            Debug.Log("Aguardando emoções...");

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

        // Analisa os dados JSON
        ProcessJsonData(jsonData);

        // Fecha a conexão com o cliente
        client.Close();

        // Continua escutando por novos clientes
        server.BeginAcceptTcpClient(AcceptClient, server);
    }

    void ProcessJsonData(string jsonData)
    {
        currentEmotions = JsonUtility.FromJson<EmotionData>(jsonData);
        newData = true;
        // Debug.Log($"Happy: {currentEmotions.Happy}, Sad: {currentEmotions.Sad}, Angry: {currentEmotions.Angry}, Scary: {currentEmotions.Scary}");
    }

    public EmotionData GetEmotions(){
        var value = newData ? currentEmotions : null;
        newData = false;
        return value;
    }

    void OnApplicationQuit()
    {
        isRunning = false;
        server.Stop();
    }
}
