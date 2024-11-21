using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GameManager : MonoBehaviour
{
    [HideInInspector]
    public GameObject player, dog, colorFilter, audioManager;
    
    public static GameManager instance;
    private EmotionManager emotionManager;

    EmotionManager.EmotionData emotionData;
    private string lastEmotion = "NEUTRAL";
    private string emotion = "NEUTRAL";

    void Awake(){
        if(instance == null)
        instance = this;
        
        player = GameObject.Find("Player");
        dog = GameObject.Find("Dog");
    }

    // Start is called before the first frame update
    void Start()
    {
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

    public void AttackPlayer(int damage){
        player.GetComponent<PlayerController>().Hurt(damage);
    }

    public void AttackDog(int damage){
        dog.GetComponent<DogController>().Hurt(damage);
    }
    
}
