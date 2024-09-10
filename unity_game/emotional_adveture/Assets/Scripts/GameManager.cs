using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GameManager : MonoBehaviour
{
    private EmotionManager emotionManager;

    private float bound = 0.7f;
    private float happyAcc = 0.0f,
        sadAcc = 0.0f,
        angryAcc = 0.0f,
        scaryAcc = 0.0f,
        neutralAcc = 0.0f;

    private float timeToEmotion = 0.05f;

    EmotionManager.EmotionData emotions;
    private string emotion = "NEUTRAL";

    // Start is called before the first frame update
    void Start()
    {
        emotionManager = GetComponent<EmotionManager>();
    }

    // Update is called once per frame
    void Update()
    {
        UpdateEmotions();
        Debug.Log(happyAcc + " " + emotion);
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
    }
}
