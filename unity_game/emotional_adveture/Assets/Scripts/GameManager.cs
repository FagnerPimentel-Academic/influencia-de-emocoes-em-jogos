using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GameManager : MonoBehaviour
{
    public static GameManager instance;
    private GameObject player, colorFilter, audioManager;
    private EmotionManager emotionManager;

    EmotionManager.EmotionData emotionData;
    private string lastEmotion = "NEUTRAL";
    private string emotion = "NEUTRAL";

    void Awake(){
        if(instance == null)
        instance = this;
    }

    // Start is called before the first frame update
    void Start()
    {
        player = GameObject.Find("Player");
        colorFilter = GameObject.Find("Color Filter");
        audioManager = GameObject.Find("Audio Manager");
        emotionManager = GetComponent<EmotionManager>();
    }

    // Update is called once per frame
    void Update()
    {
        UpdateEmotions();
        
    }

    void UpdateEmotions()
    {
        emotionData = emotionManager.GetEmotions();

        if (emotionData != null)
            emotion = emotionData.emotion;

        if (emotion != lastEmotion)
        {
            Debug.Log(emotion);
            lastEmotion = emotion;
            player.GetComponent<PlayerController>().ApplyEmotion(emotion);
            colorFilter.GetComponent<ColorFilterController>().ApplyEmotion(emotion);
            audioManager.GetComponent<AudioManager>().ApplyEmotion(emotion);
        }
    }
}
