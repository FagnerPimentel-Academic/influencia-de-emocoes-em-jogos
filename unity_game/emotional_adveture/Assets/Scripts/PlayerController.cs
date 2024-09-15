using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerController : MonoBehaviour
{
    public float speed;
    public float jumpForce;
    public int maxJumps;

    private bool isLanded = true;
    private int jumps = 0;

    Dictionary <string, Color> emotionPerColor = new Dictionary<string, Color>();

    private SpriteRenderer spriteRenderer;
    private Rigidbody2D rb2d;

    // Start is called before the first frame update
    void Start()
    {
        spriteRenderer = GetComponent<SpriteRenderer>();
        rb2d = GetComponent<Rigidbody2D>();

        emotionPerColor.Add("NEUTRAL", Color.white);
        emotionPerColor.Add("HAPPY", Color.green);
        emotionPerColor.Add("SAD", Color.blue);
        emotionPerColor.Add("ANGRY", Color.red);
        emotionPerColor.Add("SCARY", Color.yellow);
    }

    // Update is called once per frame
    void Update()
    {
        Movement();
    }

    private void OnCollisionEnter2D(Collision2D collision)
    {
        if (collision.collider.CompareTag("Ground"))
        {
            isLanded = true;
            jumps = 0;
        }
    }

    public void ApplyEmotion(string emotion){
        spriteRenderer.color = emotionPerColor[emotion];
    }

    private void Movement(){

        var hDirection = Input.GetAxisRaw("Horizontal");
        var vDirection = Input.GetAxisRaw("Vertical");
        var jumpPressed = Input.GetButtonDown("Jump");

        if (hDirection == 1f)
        {
            spriteRenderer.flipX = false;
            transform.position = new Vector2(
                transform.position.x + speed * Time.deltaTime,
                transform.position.y
            );
        }
        else if (hDirection == -1f)
        {
            spriteRenderer.flipX = true;
            transform.position = new Vector2(
                transform.position.x - speed * Time.deltaTime,
                transform.position.y
            );
        }

        if (vDirection == 1f) { }
        else if (vDirection == -1f) { }

        if (jumpPressed)
        {
            if (isLanded)
            {
                isLanded = false;
                rb2d.AddForce(new Vector2(0, jumpForce), ForceMode2D.Impulse);
            }
            else if (jumps < maxJumps)
            {
                rb2d.velocity = new Vector2(rb2d.velocity.x, 0);
                rb2d.AddForce(new Vector2(0, jumpForce), ForceMode2D.Impulse);
            }

            jumps++;
        }

    }
}
