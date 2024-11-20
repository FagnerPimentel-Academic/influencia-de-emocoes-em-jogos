using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class AudioManager : MonoBehaviour
{
    private AudioSource audioSource0, audioSource1;
    private int playingAudioSource = 0;
    public static AudioManager instance;
    public AudioClip neutral, happy, sad, angry, fear;
    Dictionary <string, AudioClip> emotionAudioClip = new Dictionary<string, AudioClip>();


    void Awake(){
        if(instance == null)
        instance = this;

    }

    // Start is called before the first frame update
    void Start()
    {
        emotionAudioClip.Add("NEUTRAL", neutral);
        emotionAudioClip.Add("HAPPY", happy);
        emotionAudioClip.Add("SAD", sad);
        emotionAudioClip.Add("ANGRY", angry);
        emotionAudioClip.Add("FEAR", fear);

        audioSource0 = gameObject.AddComponent<AudioSource>();
        audioSource1 = gameObject.AddComponent<AudioSource>();

        SwapTrack(neutral);
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void ApplyEmotion(string emotion){
        if(emotionAudioClip.ContainsKey(emotion))
            SwapTrack(emotionAudioClip[emotion]);
        else
            SwapTrack(neutral);
    }

    public void SwapTrack(AudioClip newClip){
        StopAllCoroutines();
        StartCoroutine(FadeTrack(newClip));
    }

    private IEnumerator FadeTrack(AudioClip newClip){
        float timeToFade = 1f;
        float timeElapsed = 0;

        switch(playingAudioSource){
            case 0:
                audioSource1.clip = newClip;
                audioSource1.Play();
                playingAudioSource = 1;

                while(timeElapsed < timeToFade){
                    audioSource1.volume = Mathf.Lerp(0, 1, timeElapsed / timeToFade);
                    audioSource0.volume = Mathf.Lerp(1, 0, timeElapsed / timeToFade);
                    timeElapsed += Time.deltaTime;
                    yield return null;
                }

                audioSource0.Stop();
            break;

            case 1:
                audioSource0.clip = newClip;
                audioSource0.Play();
                playingAudioSource = 0;

                while(timeElapsed < timeToFade){
                    audioSource0.volume = Mathf.Lerp(0, 1, timeElapsed / timeToFade);
                    audioSource1.volume = Mathf.Lerp(1, 0, timeElapsed / timeToFade);
                    timeElapsed += Time.deltaTime;
                    yield return null;
                }

                audioSource1.Stop();
            break;
        }

        

    }
    
}
