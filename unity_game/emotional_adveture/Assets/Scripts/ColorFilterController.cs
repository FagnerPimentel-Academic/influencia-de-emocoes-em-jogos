using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ColorFilterController : MonoBehaviour
{
    private SpriteRenderer spriteRenderer;
    
    Dictionary <string, Color> emotionPerColor = new Dictionary<string, Color>();

    // Start is called before the first frame update
    void Start()
    {
        spriteRenderer = GetComponent<SpriteRenderer>();

        float alpha = 0.08f;
        emotionPerColor.Add("NEUTRAL", new Color(1f, 1f, 1f, 0f));      // Branco
        emotionPerColor.Add("HAPPY", new Color(0f, 1f, 0f, alpha));     // Verde
        emotionPerColor.Add("SAD", new Color(0.6f, 0.6f, 0.6f, alpha)); // Cinza
        emotionPerColor.Add("ANGRY", new Color(1f, 0f, 0f, alpha));     // Vermelho
        emotionPerColor.Add("FEAR", new Color(0f, 0f, 1f, alpha));     // Azul
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void ApplyEmotion(string emotion){
        StartCoroutine(FadeToColor(emotionPerColor[emotion], 2f));
    }

    private IEnumerator FadeToColor(Color targetColor, float duration)
    {
        Color startColor = spriteRenderer.color;

        for (float t = 0; t < 1; t += Time.deltaTime / duration)
        {
            spriteRenderer.color = Color.Lerp(startColor, targetColor, t);
            yield return null;
        }

        spriteRenderer.color = targetColor;
    }
}
