using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GameManager : MonoBehaviour
{
    public static GameManager instance;
    private GameObject player, colorFilter, audioManager;
    private EmotionManager emotionManager;

    private float bound = 0.7f;
    private float happyAcc = 0.0f,
        sadAcc = 0.0f,
        angryAcc = 0.0f,
        scaryAcc = 0.0f,
        neutralAcc = 0.0f;

    private float timeToEmotion = 0.05f;

    EmotionManager.EmotionData emotions;
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
        emotions = emotionManager.GetEmotions();

        if (emotions != null)
        {
            if (emotions.Happy > bound)
            {
                happyAcc += Time.deltaTime;
            }
            else
            {
                happyAcc = 0.0f;
            }

            if (emotions.Sad > bound)
            {
                sadAcc += Time.deltaTime;
            }
            else
            {
                sadAcc = 0.0f;
            }

            if (emotions.Angry > bound)
            {
                angryAcc += Time.deltaTime;
            }
            else
            {
                angryAcc = 0.0f;
            }

            if (emotions.Scary > bound)
            {
                scaryAcc += Time.deltaTime;
            }
            else
            {
                scaryAcc = 0.0f;
            }

            if ((happyAcc + sadAcc + angryAcc + scaryAcc) > 0.0f)
            {
                neutralAcc = 0;
            }
            else
            {
                neutralAcc += Time.deltaTime;

                if (neutralAcc > timeToEmotion)
                {
                    emotion = "NEUTRAL";
                }
            }
        }

        if (happyAcc > timeToEmotion)
        {
            emotion = "HAPPY";
        }

        if (sadAcc > timeToEmotion)
        {
            emotion = "SAD";
        }

        if (angryAcc > timeToEmotion)
        {
            emotion = "ANGRY";
        }

        if (scaryAcc > timeToEmotion)
        {
            emotion = "SCARY";
        }

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
