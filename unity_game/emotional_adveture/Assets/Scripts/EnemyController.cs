using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class EnemyController : MonoBehaviour
{
    public int hp;
    public GameObject deathFXPrefab;
    private GameObject deathFX;

    private SpriteRenderer spriteRenderer;
    private Rigidbody2D rb2d;

    // Start is called before the first frame update
    void Start()
    {
        spriteRenderer = GetComponent<SpriteRenderer>();
        rb2d = GetComponent<Rigidbody2D>();
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void Hurt(int damage)
    {
        hp -= damage;

        spriteRenderer.color = Color.red;
        Invoke("ResetColor", 0.1f);

        if (hp < 1)
        {
            spriteRenderer.enabled = false;
            deathFX = Instantiate(deathFXPrefab, transform.position, Quaternion.identity);
            Invoke("Death", 0.5f);
        }

        if(spriteRenderer.flipX){
            rb2d.AddForce(new Vector2(-4, 0), ForceMode2D.Impulse);
        }else{
            rb2d.AddForce(new Vector2(4, 0), ForceMode2D.Impulse);
        }
    }

    void Death(){
        Destroy(deathFX);
        Destroy(gameObject);
    }

    private void ResetColor()
    {
        spriteRenderer.color = Color.white;
    }


}
